"""Atomic persistence for the policy and training checkpoint."""

import os
import pickle

from config import CHECKPOINT_FILE, Q_TABLE_FILE


def _atomic_pickle_dump(value, filename):
    temporary_filename = filename + ".tmp"
    with open(temporary_filename, "wb") as file:
        pickle.dump(value, file)
        file.flush()
        os.fsync(file.fileno())
    os.replace(temporary_filename, filename)


def save_q_table(q_table, filename=Q_TABLE_FILE):
    _atomic_pickle_dump(q_table, filename)


def load_q_table(filename=Q_TABLE_FILE):
    with open(filename, "rb") as file:
        return pickle.load(file)


def save_checkpoint(q_table, iteration, mode, filename=CHECKPOINT_FILE):
    checkpoint = {
        "q_table": q_table,
        "iteration": iteration,
        "mode": mode,
    }
    _atomic_pickle_dump(checkpoint, filename)


def load_checkpoint(filename=CHECKPOINT_FILE):
    try:
        with open(filename, "rb") as file:
            checkpoint = pickle.load(file)
    except (OSError, EOFError, pickle.UnpicklingError):
        return None

    required_keys = ("q_table", "iteration", "mode")
    if not isinstance(checkpoint, dict):
        return None
    if not all(key in checkpoint for key in required_keys):
        return None
    return checkpoint

