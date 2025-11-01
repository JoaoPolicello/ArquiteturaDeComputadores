from ngram_score import ngram_score

probababilitiesFile = 'probabilidades_palavras.txt'
codedFile = 'mensagem_codificada.txt'
ngram_score = ngram_score(probababilitiesFile)

class caesar_solver():
    def __init__(self):
        binaryLetters = open(codedFile).read().split('  ')
        decimalLetters = [int(b,2) for b in binaryLetters]

        bestGuessScore = float('-inf')
        bestGuessMessage = ""

        for key in range(26):
            decodedMessage = ''.join([mapNewLetter(d, key) for d in decimalLetters])
            score = ngram_score.score(decodedMessage)
            if score > bestGuessScore:
                bestGuessScore = score
                bestGuessMessage = decodedMessage

        print(f'Best Score: {bestGuessScore}')
        print(f'Message: {bestGuessMessage}')

def mapNewLetter(letter, key):
    if 65 <= letter <= 90:
        return chr(((letter - 65 + key) % 26) + 65)
    else:
        return chr(letter)

if __name__ == "__main__":
    solver = caesar_solver()