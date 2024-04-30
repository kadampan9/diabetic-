from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
import psycopg2.extras
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'font.html')


def predict(request):
    return render(request, 'predict.html')


def ads(request):
    return render(request, 'ads.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
import psycopg2

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

from django.shortcuts import render, redirect
from django.db import connection

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        # Check if the username or email already exists in the database
        conn = psycopg2.connect(database="diabetes_data", user="postgres", password="root",
                                host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute("SELECT * FROM signup WHERE \"Username\" = %s AND \"Password\" = %s", (username, password))
        user = cur.fetchone()

        if user is not None:
            # Authentication successful, redirect to the home page
            return redirect('home')  # Assuming 'home' is the name of the URL pattern for the home page
        else:
            # Authentication failed, show login page with error message
            messages.error(request, 'Incorrect username or password')
            return render(request, 'signup.html')  # Render the signin page template with error message

    return render(request, 'signup.html')  # Render the signin page template


def signup(request):
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        body = request.POST.get('password')

        # Check if the username or email already exists in the database
        conn = psycopg2.connect(database="diabetes_data", user="postgres", password="root",
                                host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute("SELECT * FROM signup WHERE \"Username\" = %s OR \"Email\" = %s", (name, email))
        result = cur.fetchone()

        if result:
            error_message = "Username or email already exists. Please choose a different one."
            return render(request, 'signup.html', {'error_message': error_message})
        else:
            cur.execute(
                "INSERT INTO signup (\"Username\", \"Email\", \"Password\") VALUES (%s, %s, %s)",
                (name, email, body))
            conn.commit()
            conn.close()
            return render(request, 'signup.html')

    return render(request, 'signup.html')


def result(request):
    data = pd.read_csv(r"C:\Users\ADMIN\Desktop\Muruga\diabetes.csv")

    X = data.drop("Outcome", axis=1)
    Y = data['Outcome']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    X_train

    model = LogisticRegression()
    model.fit(X_train, Y_train)

    n1 = request.POST.get('n1')
    n2 = request.POST.get('n2')
    n3 = request.POST.get('n3')
    n4 = request.POST.get('n4')
    n5 = request.POST.get('n5')
    n6 = request.POST.get('n6')
    n7 = request.POST.get('n7')
    n8 = request.POST.get('n8')
    val1 = float(n1)
    val2 = float(n2)
    val3 = float(n3)
    val4 = float(n4)
    val5 = float(n5)
    val6 = float(n6)
    val7 = float(n7)
    val8 = float(n8)

    pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])
    results1 = ""
    if pred == [1]:
        results1 = "positive"
    else:
        results1 = "Negative"
        # Get 'name' and 'email' from the form


    if request.method == 'POST':
        n1 = request.POST['n1']
        n2 = request.POST['n2']
        n3 = request.POST['n3']
        n4 = request.POST['n4']
        n5 = request.POST['n5']
        n6 = request.POST['n6']
        n7 = request.POST['n7']
        n8 = request.POST['n8']
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="diabetes_data", user="postgres", password="root",
                                host="localhost", port="5432")
        # Create a cursor object to interact with the database
        cur = conn.cursor()
        # Insert the data into the database
        cur.execute(
            "INSERT INTO diabetes ( \"Pregnancies\" ,\"Glucose\", \"BloodPressure\", \"SkinThickness\" , \"Insulin\", \"BMI\" , \"DiabetesPedigreeFunction\" , \"Age\" ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (n1, n2, n3, n4, n5, n6, n7, n8))
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return render(request, "predict.html", {"result2": results1})

    else:
        return render(request, "predict.html", {"result2": results1})



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        body = request.POST.get('body')
        print(name, email, body)
        send_mail(
            'Diabetic predict project ',
            name + "-" + body + email, email,
            ['makeswarankadampan@gmail.com'],
            fail_silently=False,
        )
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="diabetes_data", user="postgres", password="root",
                                host="localhost", port="5432")

        # Create a cursor object to interact with the database
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO conactus ( \"Name\" ,\"Email\", \"Body\" ) VALUES (%s, %s, %s)",
            (name, email, body))
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    return render(request, 'contact.html')

from django.contrib.auth import logout  # Import the logout function

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page

# views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
import psycopg2
import psycopg2.extras
from django.contrib import messages

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(database="diabetes_data", user="postgres", password="root",
                                host="localhost", port="5432")
        cur = conn.cursor()

        # Check if the username and email exist in the database
        cur.execute("SELECT * FROM signup WHERE \"Username\" = %s AND \"Email\" = %s", (username, email))
        user = cur.fetchone()

        if user is not None:
            # Update the password for the user
            cur.execute("UPDATE signup SET \"Password\" = %s WHERE \"Username\" = %s", (new_password, username))
            conn.commit()
            conn.close()
            messages.success(request, 'Password reset successfully')
            return redirect('login')  # Redirect to the login page after successful password reset
        else:
            # If user not found, show error message
            messages.error(request, 'Incorrect username or email')
            return render(request, 'password_reset.html')  # Render the password reset page with error message

    return render(request, 'password_reset.html')  # Render the password reset page

# Your other views here...
