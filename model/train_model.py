import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.manual_seed(100)


def Adam_optimizer(model, learning_rate=0.001):
    return Adam(model.parameters(), lr=learning_rate)


def loss_function():
    return nn.L1Loss()


def euclidean_distace(true_value, predicted_value):
    return torch.sqrt(torch.sum(torch.square(true_value - predicted_value)))


def train(
    model,
    train_dataloader,
    val_dataloader,
    model_save_folder_path,
    stem_name="vocal",
    epoch=10,
    learning_rate=0.001,
):
    """To train and save the best, latest model checkpoint

    Parameters
    ----------
    model : object
        object of Unet
    train_dataloader : dataloader
    val_dataloader : dataloader
    model_save_folder_path : string
        path of the folder where the model should be saved
    stem_name : str, optional
        train for respective stem model (bass, drum, vocal, instrumental), by default 'vocal'
    epoch : int, optional, by default 10

    learning_rate : float, optional, by default 0.001

    Returns
    -------
    tuple (training_loss | list, training_distance | list, validation_loss | list, validation_distance | list)
        contain matrices value of training and validation
    """
    try:
        if stem_name == "bass":
            index = 0
        elif stem_name == "drum":
            index = 1
        elif stem_name == "vocal":
            index = 2
        elif stem_name == "instrumental":
            index = 3
        else:
            print(
                f"Provided stem name {stem_name} is not among (bass, drum, vocal, instrumental)"
            )

        optimizer = Adam_optimizer(model, learning_rate=learning_rate)
        loss_fn = loss_function()
        model.train()
        if model_save_folder_path[-1] == "/":
            model_save_folder_path = model_save_folder_path[:-1]

        if os.path.exists(
            model_save_folder_path + f"/{stem_name}_latest_model_checkpoint.pt"
        ):
            model_checkpoint = torch.load(
                model_save_folder_path + f"/{stem_name}_latest_model_checkpoint.pt",
                map_location=device,
            )
            model.load_state_dict(model_checkpoint["model_state_dict"])
            optimizer.load_state_dict(model_checkpoint["optimizer_state_dict"])
            check_point_epoch = model_checkpoint["epoch"] + 1
            LOSS = model_checkpoint["loss"]
            training_loss = LOSS["training_loss"]
            training_distance = LOSS["training_distance"]
            validation_loss = LOSS["validation_loss"]
            validation_distance = LOSS["validation_distance"]
            min_loss = min(validation_loss)
        else:
            model.to(device)
            training_loss = []
            validation_loss = []
            training_distance = []
            validation_distance = []
            check_point_epoch = 1
            min_loss = 1000000
        for i in range(check_point_epoch, epoch + check_point_epoch):
            train_loss = []
            val_loss = []
            train_distance = []
            val_distance = []
            train_loop = tqdm(train_dataloader, leave=True)
            for mixture, bass, drum, vocal, instumental in train_loop:
                stem = bass, drum, vocal, instumental
                train_loop.set_description(f"Epoch {i}")
                optimizer.zero_grad()
                y = model(mixture)
                loss = loss_fn(stem[index], torch.mul(y, mixture))
                loss.backward()
                optimizer.step()

                # pred = torch.mul(mixture, y)
                distance = euclidean_distace(stem[index], torch.mul(y, mixture))
                train_loss.append(loss.item())
                train_distance.append(distance.item())

                train_loop.set_postfix(
                    train_loss=sum(train_loss) / len(train_loss),
                    train_euclidean_distance=sum(train_distance) / len(train_distance),
                )

            val_loop = tqdm(val_dataloader, leave=True)
            with torch.no_grad():
                for mixture, bass, drum, vocal, instumental in val_loop:
                    stem = bass, drum, vocal, instumental
                    y = model(mixture)
                    loss = loss_fn(stem[index], torch.mul(y, mixture))

                    # pred = torch.mul(mixture, y)
                    distance = euclidean_distace(stem[index], torch.mul(y, mixture))
                    val_loss.append(loss.item())
                    val_distance.append(distance.item())

                    val_loop.set_postfix(
                        train_loss=sum(train_loss) / len(train_loss),
                        train_euclidean_distance=sum(train_distance)
                        / len(train_distance),
                        val_loss=sum(val_loss) / len(val_loss),
                        val_euclidean_distance=sum(val_distance) / len(val_distance),
                    )

            training_loss.append(sum(train_loss) / len(train_loss))
            training_distance.append(sum(train_distance) / len(train_distance))
            validation_loss.append(sum(val_loss) / len(val_loss))
            validation_distance.append(sum(val_distance) / len(val_distance))

            LOSS = {
                "training_loss": training_loss,
                "training_distance": training_distance,
                "validation_loss": validation_loss,
                "validation_distance": validation_distance,
            }
            torch.save(
                {
                    "epoch": i,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": LOSS,
                },
                model_save_folder_path + f"/{stem_name}_latest_model_checkpoint.pt",
            )
            if min_loss > validation_loss[-1]:
                min_loss = validation_loss[-1]
                torch.save(
                    model, model_save_folder_path + f"/{stem_name}_best_model.pt"
                )
                torch.save(
                    {
                        "epoch": i,
                        "model_state_dict": model.state_dict(),
                        "optimizer_state_dict": optimizer.state_dict(),
                        "loss": LOSS,
                    },
                    model_save_folder_path + f"/{stem_name}_best_model_checkpoint.pt",
                )

        return (training_loss, training_distance, validation_loss, validation_distance)
    except Exception as e:
        print(e)
        return None