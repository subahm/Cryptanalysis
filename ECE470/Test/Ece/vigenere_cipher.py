

from cryptography_algebra import convert_sentence_to_np_array_of_numbers, convert_np_array_numbers_to_sentence, maintain_length_of_keyword_with_plaintext


def encrypt(plaintext, keyword):
    """
        convert plaintext to numpy array of numbers
        increase the length of keyword to maintain same size with plaintext and convert to numpy arrays
        use Vigenere encryption function 
        return cipher text after converting numpy numbers to alphabets
    """
    plaintext_in_numbers = convert_sentence_to_np_array_of_numbers(plaintext)
    extended_keyword = maintain_length_of_keyword_with_plaintext(plaintext, keyword)
    keyword_in_numbers = convert_sentence_to_np_array_of_numbers(extended_keyword)
    encrypt_vigenere_cipher = (plaintext_in_numbers + keyword_in_numbers) % 26
    return convert_np_array_numbers_to_sentence(encrypt_vigenere_cipher).upper()

def decrypt(ciphertext, keyword):
    """
        convert ciphertext to numbers
        extend keyword to maintain same length with ciphertext
        use Vigenere decryption function
        return plain text after converting numpy numbers to alphabets
    """
    ciphertext_in_numbers = convert_sentence_to_np_array_of_numbers(ciphertext)
    extended_keyword = maintain_length_of_keyword_with_plaintext(ciphertext, keyword)
    keyword_in_numbers = convert_sentence_to_np_array_of_numbers(extended_keyword)
    decrypt_vigenere_cipher = (ciphertext_in_numbers - keyword_in_numbers) % 26
    return convert_np_array_numbers_to_sentence(decrypt_vigenere_cipher)

def crack(ciphertext, keylength, number_of_generations):
    return run_genetic_algorithm(keylength, number_of_generations, ciphertext, mutation_rate=0.2)
