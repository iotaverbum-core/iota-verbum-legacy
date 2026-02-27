#!/usr/bin/env python3
"""
Training script for formation vector regression models. Given a CSV file
containing text responses and labelled scores for each dimension, this
script fine‑tunes RandomForestRegressor models per dimension. It uses
the sentence‑transformers all‑mpnet‑base‑v2 embedder for text encoding.

Usage:
    python train_scoring_model.py --data my_dataset.csv --text-col text --out model
This will save two files: model.json (configuration) and model.models.pkl
with the trained estimators. See README for integration.
"""

import argparse
import json
import pandas as pd
import numpy as np
import joblib
from transformers import AutoTokenizer, AutoModel
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import torch
from pathlib import Path


class FormationVectorPredictor:
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2', device=None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.embedder = AutoModel.from_pretrained(model_name)
        self.embedder.eval()
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.embedder.to(self.device)
        self.dimensions = [
            'clarity', 'completeness', 'safety', 'respect',
            'accuracy', 'transparency', 'empathy', 'boundaries',
            'actionability', 'nuance', 'encourages_thinking', 'avoids_dependency'
        ]
        self.dimension_models = {}

    @torch.no_grad()
    def encode_texts(self, texts, batch_size=16):
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            encoded = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors='pt'
            ).to(self.device)
            outputs = self.embedder(**encoded)
            last_hidden = outputs.last_hidden_state
            attention = encoded['attention_mask'].unsqueeze(-1)
            masked = last_hidden * attention
            summed = masked.sum(dim=1)
            counts = attention.sum(dim=1).clamp(min=1)
            emb = (summed / counts).cpu().numpy()
            embeddings.append(emb)
        return np.vstack(embeddings)

    def fit(self, texts, labels_df):
        X = self.encode_texts(texts)
        for dim in self.dimensions:
            y = labels_df[dim].astype(float).values
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)
            val_pred = model.predict(X_val)
            mae = np.mean(np.abs(val_pred - y_val))
            print(f'Trained {dim} (MAE={mae:.3f})')
            self.dimension_models[dim] = model

    def save(self, base_path):
        base = Path(base_path)
        base.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.dimension_models, base.with_suffix('.models.pkl'))
        cfg = {
            'model_name': self.embedder.config.name_or_path,
            'dimensions': self.dimensions,
            'models_file': base.with_suffix('.models.pkl').name
        }
        with open(base.with_suffix('.json'), 'w') as f:
            json.dump(cfg, f, indent=2)


def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('--data', required=True, help='CSV file path containing text and labels')
        parser.add_argument('--text-col', default='text', help='Column name containing text')
        parser.add_argument('--out', default='formation_model', help='Output base filename')
        args = parser.parse_args()
        df = pd.read_csv(args.data)
        predictor = FormationVectorPredictor()
        texts = df[args.text_col].astype(str).tolist()
        labels = df[predictor.dimensions].copy()
        predictor.fit(texts, labels)
        predictor.save(args.out)
        print('Model saved to', args.out)


if __name__ == '__main__':
    main()