from flask import Flask, request, render_template_string
import random
import string

app = Flask(__name__)

# HTML templates
SIGNIN_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Sign In</title>
</head>
<body>
    <h1>Student Sign In</h1>
    <form method="post" action="/verify">
        <label for="sid">Student ID:</label>
        <input type="text" id="sid" name="sid" required><br><br>

        <label for="code">Sign-in Code:</label>
        <input type="text" id="code" name="code" required><br><br>

        <button type="submit">Sign in</button>
    </form>
</body>
</html>
"""


def generate_random_code(length=10):
    """Generate a random code with digits and lowercase letters"""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def read_codes_file():
    """Read codes from file into a dictionary"""
    codes = {}
    try:
        with open('codes.txt', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    codes[parts[0]] = parts[1]
    except FileNotFoundError:
        pass
    return codes


def write_codes_file(codes):
    """Write dictionary to codes.txt file"""
    with open('codes.txt', 'w') as f:
        for code, sid in codes.items():
            f.write(f"{code}\t{sid}\n")


@app.route('/codes')
def generate_codes():
    """Generate and display 100 random codes"""
    codes = {}
    for i in range(1, 101):
        codes[f"{i}{generate_random_code(9)}"] = '0'  # Prefix with number for easier testing

    # Save to file
    write_codes_file(codes)

    # Create HTML table
    table = "<table border='1'>"
    code_list = list(codes.keys())
    for row in range(20):
        table += "<tr>"
        for col in range(5):
            idx = row * 5 + col
            if idx < len(code_list):
                table += f"<td>{code_list[idx]}</td>"
        table += "</tr>"
    table += "</table>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Attendance Codes</title>
    </head>
    <body>
        <h1>Attendance Codes</h1>
        {table}
        <p>Codes have been saved to codes.txt</p>
    </body>
    </html>
    """


@app.route('/signin', methods=['GET'])
def signin_form():
    """Display the sign-in form"""
    return SIGNIN_FORM


@app.route('/verify', methods=['GET', 'POST'])
def verify_code():
    """Verify the student's code"""
    if request.method == 'GET':
        # Handle GET request (for testing)
        sid = request.args.get('sid', '')
        code = request.args.get('code', '')
    else:
        # Handle POST request
        sid = request.form.get('sid', '')
        code = request.form.get('code', '')

    codes = read_codes_file()
    signed_sid = codes.get(code, None)

    if signed_sid is None:
        message = "Wrong code entered"
    elif signed_sid == '0':
        codes[code] = sid
        write_codes_file(codes)
        message = "You are successfully signed in"
    elif sid == signed_sid:
        message = "You have signed in already"
    else:
        message = f"The code is used by {signed_sid} and cannot be shared"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sign In Result</title>
    </head>
    <body>
        <h1>Sign In Result</h1>
        <p>{message}</p>
        <a href="/signin">Back to sign in</a>
    </body>
    </html>
    """


@app.route('/attended')
def attended_list():
    """Display list of attended students"""
    codes = read_codes_file()
    attended = [sid for sid in codes.values() if sid != '0']

    if not attended:
        return "No students have signed in yet."

    return "<br>".join(attended)


if __name__ == '__main__':
    app.run(debug=True)