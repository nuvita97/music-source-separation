import torch
import torch.nn as nn
import torch.nn.functional as F


torch.manual_seed(100)


class encoder(nn.Module):
    def __init__(self, in_channel, out_channel):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channel, out_channel, kernel_size=(5, 5), stride=2, padding=1
        )
        self.batchnorm = nn.BatchNorm2d(out_channel)
        self.l_relu = nn.LeakyReLU(0.2)

    def forward(self, x):
        x = self.conv(x)
        x = self.batchnorm(x)
        x = self.l_relu(x)
        return x


class decoder(nn.Module):
    def __init__(self, in_channel, out_channel):
        super().__init__()
        self.dconv = nn.ConvTranspose2d(
            in_channel, out_channel, kernel_size=(5, 5), stride=2, padding=1
        )
        self.batchnorm = nn.BatchNorm2d(out_channel)

    def forward(self, x):
        x = self.dconv(x)
        x = self.batchnorm(x)
        return x


class UNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder1 = encoder(1, 16)
        self.encoder2 = encoder(16, 32)
        self.encoder3 = encoder(32, 64)
        self.encoder4 = encoder(64, 128)
        self.encoder5 = encoder(128, 256)
        self.encoder6 = encoder(256, 512)

        self.decoder1 = decoder(512, 256)
        self.dropout1 = nn.Dropout(0.5)
        self.relu1 = nn.ReLU()
        self.decoder2 = decoder(256 * 2, 128)
        self.dropout2 = nn.Dropout(0.5)
        self.relu2 = nn.ReLU()

        self.decoder3 = decoder(128 * 2, 64)
        self.dropout3 = nn.Dropout(0.5)
        self.relu3 = nn.ReLU()

        self.decoder4 = decoder(64 * 2, 32)
        self.relu4 = nn.ReLU()

        self.decoder5 = decoder(32 * 2, 16)
        self.relu5 = nn.ReLU()

        self.decoder6 = decoder(16 * 2, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        conv1 = self.encoder1(x)
        conv2 = self.encoder2(conv1)
        conv3 = self.encoder3(conv2)
        conv4 = self.encoder4(conv3)
        conv5 = self.encoder5(conv4)
        conv6 = self.encoder6(conv5)

        dconv1 = self.decoder1(conv6)
        dconv1 = self.dropout1(dconv1)
        dconv1 = self.relu1(dconv1)
        dconv1 = torch.concat([dconv1, conv5], dim=1)

        dconv2 = self.decoder2(dconv1)
        dconv2 = self.dropout3(dconv2)
        dconv2 = self.relu2(dconv2)
        dconv2 = torch.concat([dconv2, conv4], dim=1)

        dconv3 = self.decoder3(dconv2)
        dconv3 = self.dropout3(dconv3)
        dconv3 = self.relu3(dconv3)
        dconv3 = torch.concat([dconv3, conv3], dim=1)

        dconv4 = self.decoder4(dconv3)
        dconv4 = self.relu4(dconv4)
        dconv4 = torch.concat([dconv4, conv2], dim=1)

        dconv5 = self.decoder5(dconv4)
        dconv5 = self.relu5(dconv5)

        dconv5 = torch.concat([dconv5, conv1], dim=1)

        output = self.decoder6(dconv5)
        output = self.sigmoid(output)
        return output