# -*- coding: utf-8 -*-
"""ImageOnly_Zoobot_ResNet_v1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10ioGLQ4VjWQUDdSSAc9BD2VPSgl8Zs-Y
"""

import time
import torch
import torch.nn as nn
import timm
import pytorch_lightning as pl
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.metrics import f1_score

import timm
from zoobot.pytorch.training.finetune import FinetuneableZoobotAbstract


class ImageOnlyZoobotModelResNet(pl.LightningModule):

    def __init__(self, name: str, num_classes: int):
        super().__init__()

        # Timm 라이브러리로 사전학습된 모델 불러오기 (fc는 제거)
        self.encoder = timm.create_model(
            name,
            pretrained=True,
            num_classes=0,        # head 제거
            drop_rate=0.2,        # dropout 확률
            drop_path_rate=0.1    # stochastic depth 확률
        )

        # 모델 출력 feature 차원 자동 계산을 위한 dummy 입력
        dummy_input = torch.zeros(1, 3, 224, 224)
        with torch.no_grad():
            dummy_output = self.encoder.forward_features(dummy_input)

        # feature 벡터의 차원 확인
        feature_dim = dummy_output.reshape(1, -1).size(1)

        # layer1 ~ layer3 freeze (학습 제외)
        for i in range(1, 4):
            for param in getattr(self.encoder, f'layer{i}').parameters():
                param.requires_grad = False

        # 디버깅용: 각 파라미터가 학습되는지 여부 출력
        for name, param in self.encoder.named_parameters():
            print(f"{name:60} | requires_grad = {param.requires_grad}")

        # classification head 정의
        self.head = nn.Linear(feature_dim, num_classes)

        # 손실 함수
        self.loss_fn = nn.CrossEntropyLoss()

        # 학습 성능 기록용 리스트 초기화
        self.train_losses, self.val_losses = [], []
        self.train_accs, self.val_accs = [], []
        self.train_f1s, self.val_f1s = [], []

        # 학습 시간 측정용
        self.epoch_times = []
        self.train_start_time = None
        self.epoch_start_time = None

    def forward(self, image):
        # 특징 추출 후 flatten하여 head에 통과
        features = self.encoder.forward_features(image)
        features = features.reshape(features.size(0), -1)
        return self.head(features)

    def training_step(self, batch, batch_idx):
        image, label = batch
        logits = self(image)
        loss = self.loss_fn(logits, label)
        preds = logits.argmax(dim=1)

        # 정확도 및 F1 score 계산 (CPU에서)
        acc = (preds == label).float().mean()
        f1 = f1_score(label.cpu(), preds.cpu(), average='macro')

        # 출력 저장 (에폭 평균용)
        if not hasattr(self, 'train_step_outputs'):
            self.train_step_outputs = []

        self.train_step_outputs.append({
            'loss': loss.detach(),
            'acc': acc.detach(),
            'f1': torch.tensor(f1)
        })

        # 로그 기록
        self.log("train_loss", loss, prog_bar=True)
        self.log("train_acc", acc, prog_bar=True)
        self.log("train_f1", f1, prog_bar=True)
        return loss

    def on_train_start(self):
        # 학습 시작 시간 기록
        self.train_start_time = time.time()
        print("\n=== Training Started ===")

    def on_train_epoch_start(self):
        # 에폭 시작 시간 기록
        self.epoch_start_time = time.time()

    def on_train_epoch_end(self):
        # 에폭 단위 평균 계산
        outputs = self.train_step_outputs
        avg_loss = torch.stack([x['loss'] for x in outputs]).mean().item()
        avg_acc = torch.stack([x['acc'] for x in outputs]).mean().item()
        avg_f1 = torch.stack([x['f1'] for x in outputs]).mean().item()

        # 기록 저장
        self.train_losses.append(avg_loss)
        self.train_accs.append(avg_acc)
        self.train_f1s.append(avg_f1)

        # 시간 측정
        epoch_duration = time.time() - self.epoch_start_time
        self.epoch_times.append(epoch_duration)

        print(f"Epoch {self.current_epoch} time: {epoch_duration:.2f} sec")
        print(f"Train Loss: {avg_loss:.4f}, Train Acc: {avg_acc:.4f}, Train F1: {avg_f1:.4f}")

        self.train_step_outputs.clear()

    def validation_step(self, batch, batch_idx):
        image, label = batch
        logits = self(image)
        loss = self.loss_fn(logits, label)
        preds = logits.argmax(dim=1)

        acc = (preds == label).float().mean()
        f1 = f1_score(label.cpu(), preds.cpu(), average='macro')

        if not hasattr(self, 'val_step_outputs'):
            self.val_step_outputs = []

        self.val_step_outputs.append({
            'val_loss': loss.detach(),
            'val_acc': acc.detach(),
            'val_f1': torch.tensor(f1)
        })

        # 로그 기록
        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", acc, prog_bar=True)
        self.log("val_f1", f1, prog_bar=True)
        return loss

    def on_validation_epoch_end(self):
        # 에폭별 검증 결과 평균 계산
        outputs = self.val_step_outputs
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean().item()
        avg_acc = torch.stack([x['val_acc'] for x in outputs]).mean().item()
        avg_f1 = torch.stack([x['val_f1'] for x in outputs]).mean().item()

        self.val_losses.append(avg_loss)
        self.val_accs.append(avg_acc)
        self.val_f1s.append(avg_f1)

        print(f"Val Loss: {avg_loss:.4f}, Val Acc: {avg_acc:.4f}, Val F1: {avg_f1:.4f}")

        self.val_step_outputs.clear()

    def on_train_end(self):
        # 학습 전체 시간 측정 및 출력
        total_training_time = time.time() - self.train_start_time
        print(f"\n=== Training Finished in {total_training_time:.2f} seconds ===")
        for i, t in enumerate(self.epoch_times):
            print(f"Epoch {i}: {t:.2f} seconds")

    def configure_optimizers(self):
        # 옵티마이저 및 스케줄러 설정
        optimizer = Adam(self.parameters(), lr=0.001)
        scheduler = {
            'scheduler': ReduceLROnPlateau(
                optimizer,
                mode='min',
                factor=0.5,
                patience=3,
                verbose=True
            ),
            'monitor': 'val_loss'  # validation loss 기준으로 조정
        }
        return {"optimizer": optimizer, "lr_scheduler": scheduler}
