import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


class Neural_Network:
    def __init__(self):
        self.data_list = []
        self.extract_data()
        self.train_x, self.train_y, self.test_x, self.test_y = self.get_data_sets()
        self.input_size = len(self.train_x[0])
        self.output_size = len(set(self.train_y))
        self.hidden_layer_size = int((self.output_size + self.input_size) / 2)
        self.epochs = 500
        self.learning_rate = 0.01
        self.first_layer_limit = self.compute_current_limit(self.input_size, self.hidden_layer_size)
        self.second_layer_limit = self.compute_current_limit(self.hidden_layer_size, self.output_size)
        self.weights = []
        self.biases = []
        self.layers = []
        self.layers.append(self.input_size)
        self.layers.append(self.hidden_layer_size)
        self.layers.append(self.output_size)
        self.initialize_weights(self.first_layer_limit, self.input_size, self.hidden_layer_size)
        self.initialize_weights(self.second_layer_limit, self.hidden_layer_size, self.output_size)
        self.initialize_biases(self.hidden_layer_size)
        self.initialize_biases(self.output_size)
        self.train_neural_network()

    def compute_current_limit(self, input_size, output_size):
        limit = np.sqrt(6 / (input_size + output_size))
        return limit

    def initialize_weights(self, limit, input_size, output_size):
        current_weights = np.random.uniform(-limit, limit, size=(input_size, output_size))
        self.weights.append(current_weights)

    def initialize_biases(self, layer_size):
        biases = np.ones(layer_size) * 0.01
        self.biases.append(biases)

    def insert_biases(self, layer_size):
        biases = np.ones(layer_size) * 0.01
        self.biases.insert(-1, biases)

    def insert_weights(self, limit, input_size, output_size):
        current_weights = np.random.uniform(-limit, limit, size=(input_size, output_size))
        self.weights.insert(-1, current_weights)

    def extract_data(self):
        with open('seeds_dataset.txt', 'r') as file:
            for line in file:
                processed_line = line.strip()
                data = processed_line.split()
                numerical_data = [float(part) if i < len(data) - 1 else int(part) for i, part in enumerate(data)]
                self.data_list.append(numerical_data)
            np.random.shuffle(self.data_list)

    def get_data_sets(self):
        train_x, train_y = [], []
        test_x, test_y = [], []
        for data in self.data_list:
            rand = random.random()
            if rand < 0.8:
                train_y.append(data.pop(len(data) - 1))
                train_x.append(data)
            else:
                test_y.append(data.pop(len(data) - 1))
                test_x.append(data)
        return train_x, train_y, test_x, test_y

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        sx = self.sigmoid(x)
        return sx * (1 - sx)

    def mean_squared_error(self, y_true, y_pred):
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        return ((y_true - y_pred) ** 2).mean()

    def convert_to_one_hot(self, data_set):
        one_hot = np.zeros((len(data_set), self.output_size))
        for i in range(len(data_set)):
            for j in range(self.output_size):
                if data_set[i] == j + 1:
                    one_hot[i][j] = 1
        return one_hot

    def train_neural_network(self):
        train_loss = []
        one_hot_true_output = self.convert_to_one_hot(self.train_y)
        for i in range(self.epochs):
            output = self.backward_propagation(self.train_x)
            mse = self.mean_squared_error(one_hot_true_output, output[-1])
            print(mse)
            train_loss.append(mse)

        print("------TEST------")
        output = self.forward_propagation(self.test_x)
        one_hot_true_output = self.convert_to_one_hot(self.test_y)
        mse = self.mean_squared_error(one_hot_true_output, output[-1])
        print(f"Mean squared error: {mse}")
        predicted_classes = np.argmax(output[-1], axis=1)
        correct_predictions = np.sum(predicted_classes + 1 == self.test_y)
        incorrect = predicted_classes + 1 != self.test_y
        accuracy = correct_predictions / len(self.test_y)
        print(f"Accuracy: {accuracy}")

        last_hidden_layer_length = 1
        if accuracy < 0.9 and len(self.biases[-1]) != last_hidden_layer_length:
            # set up for a new hidden layer
            current_input_size = len(self.biases[len(self.biases) - 2])
            new_hidden_layer_size = int((self.output_size + current_input_size) / 2)
            if len(self.biases) > 2:
                second_hidden_layer_size = len(self.biases[2])
            else:
                second_hidden_layer_size = new_hidden_layer_size

            current_layer_limit = self.compute_current_limit(current_input_size, self.output_size)
            self.insert_biases(new_hidden_layer_size)
            self.insert_weights(current_layer_limit, current_input_size, self.output_size)

            # reinitialising biases and weights with the updated
            self.biases = []
            self.weights = []
            for i in range(len(self.layers) - 1):
                self.initialize_weights(self.first_layer_limit, self.input_size, self.hidden_layer_size)
                self.initialize_weights(self.second_layer_limit, self.hidden_layer_size, self.output_size)
                self.initialize_biases(self.hidden_layer_size)
                self.initialize_biases(self.output_size)

            # inserting
            current_layer_limit = self.compute_current_limit(current_input_size, self.output_size)
            self.insert_biases(new_hidden_layer_size)
            self.insert_weights(current_layer_limit, current_input_size, new_hidden_layer_size)
            self.layers.insert(-1, new_hidden_layer_size)
            self.train_neural_network()

        plt.figure()
        plt.plot(train_loss, label='Train Loss')
        plt.title('Convergence Graph')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

        pca = PCA(n_components=2)
        test_x_pca = pca.fit_transform(self.test_x)

        plt.scatter(test_x_pca[~incorrect, 0], test_x_pca[~incorrect, 1], c='green', label='Correctly Classified')
        plt.scatter(test_x_pca[incorrect, 0], test_x_pca[incorrect, 1], c='red', label='Misclassified')
        plt.xlabel('Compressed Feature 1')
        plt.ylabel('Compressed Feature 2')
        plt.legend()
        plt.title('Misclassified Compressed Points')
        plt.show()

    def forward_propagation(self, data_set):
        output = []
        layer_input = data_set
        first_layer = np.array(layer_input)
        output.append(first_layer)
        for weight, bias in zip(self.weights, self.biases):
            hidden_input = np.dot(layer_input, weight) + bias
            layer_output = self.sigmoid(hidden_input)
            output.append(layer_output)
            layer_input = layer_output
        return output

    def backward_propagation(self, data_set):
        output = self.forward_propagation(data_set)
        one_hot_true_output = self.convert_to_one_hot(self.train_y)
        d_mse_respect_layer_output = output[len(output) - 1] - one_hot_true_output
        for i in reversed(range(1, len(output))):
            d_sigmoid_respect_layer_output = self.sigmoid_derivative(output[i])
            sensitivity_of_last_equations = d_mse_respect_layer_output * d_sigmoid_respect_layer_output
            if i > 1:
                d_mse_respect_layer_output = np.dot(sensitivity_of_last_equations,
                                                    self.weights[i - 1].T) * self.sigmoid_derivative(output[i - 1])

            step_sizes_biases = np.sum(sensitivity_of_last_equations, axis=0)
            self.biases[i - 1] = self.biases[i - 1] - step_sizes_biases * self.learning_rate

            step_sizes_weights = np.dot(output[i - 1].T, sensitivity_of_last_equations)
            self.weights[i - 1] = self.weights[i - 1] - self.learning_rate * step_sizes_weights

        output = self.forward_propagation(data_set)
        return output
