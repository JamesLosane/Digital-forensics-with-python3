import argparse

def decimal_to_hex(num):
    hexa = hex(num).replace("0x", "")
    return hexa

def hex_to_decimal(hex_num):
    decimal = int(hex_num, 16)
    return decimal

def binary_to_hex(binary):
    decimal = int(binary, 2)
    hexa = hex(decimal).replace("0x", "")
    return hexa

def hex_to_binary(hex_num):
    decimal = int(hex_num, 16)
    binary = bin(decimal).replace("0b", "")
    return binary

def decimal_to_binary(num):
    binary = bin(num).replace("0b", "")
    return binary

def main():
    parser = argparse.ArgumentParser(description='Convert decimal, hexadecimal or binary numbers')
    parser.add_argument('number', type=str, help='decimal, hexadecimal or binary number')
    args = parser.parse_args()

    number = args.number

    if number.isdigit():
        decimal = int(number)
        print(f"Hexadecimal: {decimal_to_hex(decimal)}")
        print(f"Binary: {decimal_to_binary(decimal)}")
    elif number.startswith('0x'):
        hex_num = number[2:]
        print(f"Decimal: {hex_to_decimal(hex_num)}")
        print(f"Binary: {hex_to_binary(hex_num)}")
    else:
        binary = number
        print(f"Hexadecimal: {binary_to_hex(binary)}")
        print(f"Decimal: {int(binary, 2)}")

if __name__ == '__main__':
    main()
