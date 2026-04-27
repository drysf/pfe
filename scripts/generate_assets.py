"""Genere tous les artefacts (fichier chiffre, image stegano, tresor)."""
import challenge2_crypto
import challenge3_stego
import challenge5_final


def main():
    print(">> Defi 2 : generation secret.enc")
    challenge2_crypto.encrypt_to_file()
    print(">> Defi 3 : generation carte_postale.png")
    challenge3_stego.generate()
    print(">> Defi 5 : generation tresor.aes")
    challenge5_final.encrypt()
    print("\nTous les artefacts ont ete generes dans assets/.")


if __name__ == "__main__":
    main()
