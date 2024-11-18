import torch.nn as nn
import torch.nn.functional as F

class RRDBNet(nn.Module):
    def __init__(self, in_channels=3, out_channels=3, num_features=64, num_blocks=23, num_groups=1):
        super(RRDBNet, self).__init__()
        self.conv_first = nn.Conv2d(in_channels, num_features, kernel_size=3, stride=1, padding=1)
        self.RRDB_blocks = nn.Sequential(
            *[RRDB(num_features, num_groups) for _ in range(num_blocks)]
        )
        self.conv_last = nn.Conv2d(num_features, out_channels, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        out = self.conv_first(x)
        out = self.RRDB_blocks(out)
        out = self.conv_last(out)
        return out

class RRDB(nn.Module):
    def __init__(self, num_features, num_groups=1):
        super(RRDB, self).__init__()
        self.residual_group = nn.ModuleList(
            [nn.Conv2d(num_features, num_features, kernel_size=3, stride=1, padding=1) for _ in range(num_groups)]
        )
        self.scaling_factor = 0.2

    def forward(self, x):
        identity = x
        for layer in self.residual_group:
            x = F.relu(layer(x))
        return identity + self.scaling_factor * x
