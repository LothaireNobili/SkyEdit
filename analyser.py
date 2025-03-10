import os
import binascii
from html import escape

def hexdump(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    hex_lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        hex_lines.append(hex_part)
    return '\n'.join(hex_lines)

def process_all_files():
    input_dir = "data"
    output_dir = "resultat"
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        shortname = os.path.splitext(filename)[0]
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, shortname)
        hex_content = hexdump(input_path)
        with open(output_path, 'w') as f:
            f.write(hex_content)
        print(f"Hexdump enregistré dans {output_path}")

def compare_files(filename1, filename2):
    input_dir = "resultat"
    output_dir = "comparaison"
    os.makedirs(output_dir, exist_ok=True)
    
    file1 = os.path.join(input_dir, filename1)
    file2 = os.path.join(input_dir, filename2)
    output_file = os.path.join(output_dir, f"{filename1}_{filename2}.html")
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1, data2 = f1.read(), f2.read()
    
    length = max(len(data1), len(data2))
    data1 = data1.ljust(length, b'\x00')
    data2 = data2.ljust(length, b'\x00')
    
    html_content = """<html><head><style>
    body { font-family: monospace; }
    .diff { background-color: yellow; }
    .container { display: flex; }
    .column { margin-right: 20px; }
    </style></head><body>
    <div class='container'>
    <div class='column'><pre>"""
    
    for i in range(0, length, 16):
        chunk1 = data1[i:i+16]
        chunk2 = data2[i:i+16]
        
        diff_hex = ' '.join(f'<span class="diff">{b1:02X}</span>' if b1 != b2 else f'{b1:02X}' for b1, b2 in zip(chunk1, chunk2))
        
        html_content += f"{i:08X}  {diff_hex}\n"
    
    html_content += "</pre></div><div class='column'><pre>"
    
    for i in range(0, length, 16):
        chunk1 = data1[i:i+16]
        chunk2 = data2[i:i+16]
        
        diff_hex = ' '.join(f'<span class="diff">{b2:02X}</span>' if b1 != b2 else f'{b2:02X}' for b1, b2 in zip(chunk1, chunk2))
        
        html_content += f"{i:08X}  {diff_hex}\n"
    
    html_content += "</pre></div></div></body></html>"
    
    with open(output_file, 'w') as f:
        f.write(html_content)
    print(f"Comparaison enregistrée dans {output_file}")

if __name__ == "__main__":
    print("Que voulez-vous faire ?")
    print("1. Extraire les données de tous les fichiers dans 'data' en hexadécimal")
    print("2. Comparer deux fichiers dans 'resultat' et générer un rapport HTML")
    choice = input("Votre choix (1/2) : ")
    
    if choice == "1":
        process_all_files()
    elif choice == "2":
        filename1 = input("Entrez le nom du premier fichier : ")
        filename2 = input("Entrez le nom du second fichier : ")
        compare_files(filename1, filename2)
    else:
        print("Choix invalide.")
