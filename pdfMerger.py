from pypdf import PdfMerger
import os
import ssl
import certifi
import httpx
import urllib.request
import sys

### Function to create SSL context
def create_ssl_context():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    # run `openssl s_client -showcerts -servername api.openai.com -connect api.openai.com:443 </dev/null` and save output to a file `cert.pem` in the same directory as this notebook
    custom_cert_path = 'cert.pem'
    if os.path.exists(custom_cert_path):
        ssl_context.load_verify_locations(custom_cert_path)
    else:
        print(f"Warning: Custom certificate file not found at {custom_cert_path}")

    return ssl_context


# links = ["https://zhiting.ucsd.edu/teaching/dsc190fall2024/assets/lectures/dsc190fall2024-lecture4-llm.pdf", "https://zhiting.ucsd.edu/teaching/dsc190fall2024/assets/lectures/dsc190fall2024-lecture5-ssl.pdf", "https://zhiting.ucsd.edu/teaching/dsc190fall2024/assets/lectures/dsc190fall2024-lecture6-ssl.pdf", "https://zhiting.ucsd.edu/teaching/dsc190fall2024/assets/lectures/dsc190fall2024-lecture7-improving-llm.pdf", "https://zhiting.ucsd.edu/teaching/dsc190fall2024/assets/lectures/dsc190fall2024-lecture8-improving-llm.pdf"]

def main():

    args = sys.argv[1:]
    links = []

    for l in args:
        if l[:-3] == "pdf":
            links.append(l)

    pdf = []
    for idx,url in enumerate(links):
        response = urllib.request.urlopen(url, context=create_ssl_context())
        file = open(f"pdf{idx}.pdf", 'wb+')
        file.write(response.read())
        file.close()
        pdf.append(f"pdf{idx}.pdf")
        print("Completed link: ", url)
        print(f"Saved in file pdf{idx}")

    dirpath = '/Users/angtsai/Downloads/UCSD'
    merger = PdfMerger()
    for file in pdf:
        merger.append(file)
        os.remove(os.path.join(dirpath, file))
    merger.write("final_res_118.pdf")
    merger.close()
    print("Done! Merged pdf result saved in final_res.pdf")

if __name__ == "__main__":
    main()

