import argparse

from Hybrid_system.assymetric import Assymetric
from Hybrid_system.symetric import Symetric
from Hybrid_system.work_with_json import WorkFile
from Hybrid_system.serialization_and_deserialization import Serealization


def main():
    assymetric = Assymetric()
    symetric = Symetric()
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-gen_s", "--symetric", type=str, help="Генерация симметричного ключа"
    )
    group.add_argument(
        "-gen_a", "--assymetric", type=str, help="Генерация ассиметричного ключа"
    )
    group.add_argument(
        "-gen_e",
        "--encrypted_symetric",
        type=str,
        help="Шифрование симметричного ключа",
    )
    group.add_argument(
        "-gen_d",
        "--decrypted_symetric",
        type=str,
        help="дешифрование симметричного ключа",
    )
    group.add_argument(
        "-enc", "--encryption", type=str, help="Запускает режим шифрования"
    )
    group.add_argument(
        "-dec", "--decryption", type=str, help="Запускает режим дешифрования"
    )
    parser.add_argument(
        "work_file", type=str, help="Путь к json-файлу с настройками"
    )
    args = parser.parse_args()
    work_file = WorkFile.read_json_file(args.work_file)
    match args:
        case args if args.symetric:
            key_length = int(input("Введите желаемую длину ключа (64, 128 или 192): "))
            symmetric_key = symetric.generate_symmetric_key(key_length)
            Serealization.serialize_symmetric_key(symmetric_key,work_file["symmetric_key"])
        case args if args.assymetric:
            public_key, private_key = assymetric.generate_assymetric_keys()
            Serealization.serialize_public_key(public_key, work_file["public_key"])
            Serealization.serialize_private_key(private_key, work_file["secret_key"])
        case args if args.encrypted_symetric:
            Assymetric.encrypt_symmetric_key_with_public_key(
                work_file["symmetric_key"],
                work_file["public_key"],
                work_file["encrypted_symmetric_key"],
            )
        case args if args.decrypted_symetric:
            Assymetric.decrypt_symmetric_key(
                work_file["encrypted_symmetric_key"],
                work_file["secret_key"],
                work_file["decrypted_symmetric_key"],
            )

        case args if args.encryption:
            Symetric.encrypt_text_symmetric_key(
                work_file["initial_file"],
                work_file["symmetric_key"],
                work_file["encrypted_file"],
            )
        case args if args.decryption:
            Symetric.decrypt_text_symmetric(
                work_file["encrypted_file"],
                work_file["symmetric_key"],
                work_file["decrypted_file"],
            )


if __name__ == "__main__":
    main()
