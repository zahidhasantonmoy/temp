# LSTM Next Word Predictor
# Based on the concepts demonstrated in the CampusX YouTube video
# "LSTM | Part 3 | Next Word Predictor Using | CampusX"

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.utils import to_categorical
import numpy as np
import time # For demonstration purposes in text generation

# --- 1. Data Preparation and Preprocessing ---

# Sample text data (replace with your own text corpus)
# In the video, this was copied from an FAQ page.
# For a real application, you'd use a larger dataset.
text_data = """
What is your name?
My name is AI.
What can you do?
I can chat with you.
What is LSTM?
LSTM stands for Long Short-Term Memory.
It is a type of recurrent neural network.
LSTMs are good for sequence prediction problems.
How does LSTM work?
It uses gates to control the flow of information.
What are common applications of LSTM?
Natural language processing, speech recognition, and time series analysis.
Thank you for the information.
You are welcome.
"""

# Split the text into lines (sentences or phrases)
corpus = text_data.lower().split('\n')
# Filter out empty lines that might result from splitting
corpus = [line for line in corpus if line.strip()]

# Initialize the Tokenizer
# num_words: the maximum number of words to keep, based on word frequency.
# oov_token: token to be used for out-of-vocabulary words during text_to_sequences calls
tokenizer = Tokenizer(oov_token="<oov>")
tokenizer.fit_on_texts(corpus)

# Get the total number of words in the vocabulary
total_words = len(tokenizer.word_index) + 1 # Add 1 for the <oov> token or padding

# Create input sequences
input_sequences = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

if not input_sequences:
    print("No input sequences were generated. Check your text_data and processing steps.")
    # Handle the case where no sequences are generated, e.g., by exiting or raising an error.
    # For this example, we'll create a dummy sequence to avoid errors in subsequent steps,
    # but in a real scenario, you should investigate why no sequences were created.
    # This can happen if your corpus is too small or sentences are too short.
    if total_words > 1 :
         input_sequences.append([1,1]) # Dummy sequence if vocab exists
    else:
        print("Vocabulary is also empty. Cannot proceed.")
        exit()


# Pad sequences to the same length
max_sequence_len = max([len(x) for x in input_sequences])
padded_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# Create predictors (X) and labels (y)
# X will be all words except the last one in each sequence
# y will be the last word in each sequence
X = padded_sequences[:, :-1]
labels = padded_sequences[:, -1]

# Convert labels to one-hot encoding
# The number of classes is total_words
y = to_categorical(labels, num_classes=total_words)

print(f"Total words (vocabulary size): {total_words}")
print(f"Max sequence length: {max_sequence_len}")
if X.size > 0:
    print(f"Shape of X: {X.shape}")
    print(f"Shape of y: {y.shape}")
else:
    print("X is empty. Cannot determine input shape for the model.")
    exit()

# --- 2. Building the LSTM Model ---

model = Sequential()
# Embedding layer
# input_dim: size of the vocabulary (total_words)
# output_dim: dimension of the dense embedding (e.g., 100)
# input_length: length of input sequences (max_sequence_len - 1, because X is one less)
model.add(Embedding(input_dim=total_words, output_dim=100, input_length=max_sequence_len-1))

# LSTM layer
# units: number of LSTM units (e.g., 150)
model.add(LSTM(units=150))

# Dense output layer
# units: number of output classes (total_words)
# activation: 'softmax' for multi-class classification
model.add(Dense(units=total_words, activation='softmax'))

# Print model summary
model.summary()

# --- 3. Compiling the Model ---

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# --- 4. Training the Model ---
# Note: Training can take a significant amount of time, especially with larger datasets and more epochs.
# For this demonstration, we'll use a small number of epochs.
print("\nStarting model training...")
try:
    history = model.fit(X, y, epochs=100, verbose=1) # Increased epochs for better learning on small data
    print("Model training completed.")
except Exception as e:
    print(f"An error occurred during training: {e}")
    print("Please ensure your input data (X, y) is correctly shaped and not empty.")

# --- 5. Making Predictions (Next Word Generation) ---

def generate_text(seed_text, next_words, model, tokenizer, max_sequence_len):
    """
    Generates a sequence of text given a seed text.
    """
    output_text = seed_text
    print(f"\nGenerating text with seed: '{seed_text}' for {next_words} words...")
    for _ in range(next_words):
        # Tokenize the current text
        token_list = tokenizer.texts_to_sequences([output_text])[0]
        # Pad the sequence
        padded_token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')

        # Predict the next word
        if padded_token_list.size == 0: # Should not happen if seed_text is valid
            print("Warning: Padded token list is empty. Cannot predict.")
            break

        predicted_probabilities = model.predict(padded_token_list, verbose=0)
        # Get the index of the word with the highest probability
        # Using argmax might lead to repetitive text. For more diverse generation,
        # you could sample from the probability distribution.
        predicted_index = np.argmax(predicted_probabilities, axis=-1)[0]

        # Convert the index back to a word
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break
        
        if not output_word: # If word not found (e.g., predicted index 0 if not in word_index)
            print(f"Warning: Predicted index {predicted_index} not found in tokenizer.word_index.")
            break # Stop generation if word not found

        output_text += " " + output_word
        print(output_text) # Print step-by-step generation
        time.sleep(0.5) # Add a small delay for visual effect

    return output_text

# Example of generating text:
# Ensure the model has been trained before calling this.
if 'history' in locals() and history: # Check if training happened
    print("\n--- Text Generation Example ---")
    seed = "what is"
    generated_sequence = generate_text(seed, 5, model, tokenizer, max_sequence_len)
    print(f"\nFinal generated text: {generated_sequence}")

    seed2 = "how does lstm"
    generated_sequence2 = generate_text(seed2, 4, model, tokenizer, max_sequence_len)
    print(f"\nFinal generated text: {generated_sequence2}")
else:
    print("\nModel was not trained (or training failed). Skipping text generation.")

