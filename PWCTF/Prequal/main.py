import re

import requests


class Solution:
    @staticmethod
    def solve():
        # Get the login page
        challenge_link = r"https://prequal.pwctf.com/login.php"
        page = requests.get(challenge_link, verify=False).content

        # Extract the raw data
        regex = re.compile(r"CTF\?\ (.*)\ -->")
        raw_data = regex.findall(page)

        # Convert the raw data to binary list
        binary_line = raw_data[0].replace("30", "0").replace("31", "1").replace("62", "b")
        binary_array = [binary_line[i:i + 10] for i in range(0, len(binary_line), 10)]

        # Convert the binary data to characters and reverse it
        base64_code = "".join([chr(int(c, 2)) for c in binary_array])[::-1]

        raw_decoded = base64_code.decode("base64")

        # To be continued ...


if __name__ == '__main__':
    me = Solution()
    me.solve()
