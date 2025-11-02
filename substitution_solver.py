from random import shuffle, randint, choices
import sys
from ngram_score import ngram_score
import csv

class SubstitutionSolver:
    def __init__(self, ngram_file='probabilidades_palavras.txt', binary_file='mensagem_codificada.txt'):
        self.scorer = ngram_score(ngram_file)
        self.decimal_sequence = self._load_binary_data(binary_file)
        self.global_best_score = float('-inf')
        self.global_best_key = None
        
    def _load_binary_data(self, filename):
        with open(filename, 'r') as file:
            binary_data = file.read()
        
        tokens = binary_data.split('  ')
        return [int(token, 2) for token in tokens if token.strip()]
    
    def _create_random_alphabet_mapping(self):
        alphabet = [chr(i) for i in range(65, 91)]
        shuffle(alphabet)
        return alphabet
    
    def _score_decryption(self, decimal_sequence, key):
        text = ""

        for decimal_value in decimal_sequence:
            if 65 <= decimal_value <= 90:
                letter_index = decimal_value - 65
                text += key[letter_index]
            else:
                text += chr(decimal_value)

        return self.scorer.score(text)
    
    def _decode_with_key(self, decimal_sequence, key):
        result = ""

        for decimal_value in decimal_sequence:
            if 65 <= decimal_value <= 90:
                letter_index = decimal_value - 65
                result += key[letter_index]
            else:
                result += chr(decimal_value)

        return result
    
    def decode_binary_substitution_cipher(self, max_restarts, max_iterations, scores_csv_path=None, save_every=10):
        scores_per_iteration = []
        for restart in range(max_restarts):
            key = self._create_random_alphabet_mapping()
            local_best_score = self._score_decryption(self.decimal_sequence, key)
            iterations_without_improvement = 0
            iteration_count = 0
            
            scores_per_iteration.append((restart * max_iterations + iteration_count, local_best_score))
            
            while iterations_without_improvement < max_iterations:
                pos1 = randint(0, 25)
                pos2 = randint(0, 25)
                if pos1 == pos2:
                    continue
                key[pos1], key[pos2] = key[pos2], key[pos1]
                new_score = self._score_decryption(self.decimal_sequence, key)
                if new_score > local_best_score:
                    local_best_score = new_score
                    iterations_without_improvement = 0
                else:
                    key[pos1], key[pos2] = key[pos2], key[pos1]
                    iterations_without_improvement += 1
                iteration_count += 1
                if iteration_count % save_every == 0:
                    scores_per_iteration.append((restart * max_iterations + iteration_count, local_best_score))
            
            if local_best_score > self.global_best_score:
                self.global_best_score = local_best_score
                self.global_best_key = key.copy()
        
        if scores_csv_path:
            with open(scores_csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["iteracao", "score"])
                writer.writerows(scores_per_iteration)
        
        final_message = self._decode_with_key(self.decimal_sequence, self.global_best_key)
        return final_message


    def solve(self, max_iterations, max_restarts):
        decoded_message = self.decode_binary_substitution_cipher(max_iterations, max_restarts)
        print(f"Best score: {self.global_best_score}")
        print(f"Decoded message: {decoded_message}")
        return self.global_best_score


if __name__ == "__main__":
    max_restarts = 1
    max_iterations = 20000
    scores_csv_path = "scores_evolucao_single_run.csv"

    if len(sys.argv) > 1:
        max_restarts = int(sys.argv[1])
    if len(sys.argv) > 2:
        max_iterations = int(sys.argv[2])

    solver = SubstitutionSolver()
    decoded_message = solver.decode_binary_substitution_cipher(max_restarts, max_iterations, scores_csv_path=scores_csv_path, save_every=10)