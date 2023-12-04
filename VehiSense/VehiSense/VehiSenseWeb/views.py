from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record, Carbrand, Cartypes, Vehicle, SDG
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User  # Import the User model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import connection
import mysql.connector
import json

# Create your views here.
def about(request):
    return render(request, 'about.html')

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        # Retrieve user details from the request.user object
        user_first_name = request.user.first_name
        user_last_name = request.user.last_name
        user_email = request.user.email
        user_username = request.user.username

        # Determine the staff symbol based on is_staff
        staff_symbol = "✔️" if request.user.is_staff else "❌"

        # Execute raw SQL queries to get data directly from MySQL
        with connection.cursor() as cursor:
            # QUERY 5 AVG SCORE HIGHEST
            query = """
            SELECT country_code, AVG(sdg_index_score) as avg_sdg_index
            FROM sdg
            WHERE year BETWEEN 2000 AND 2022
            GROUP BY country_code
            ORDER BY avg_sdg_index DESC
            LIMIT 5;
            """
            cursor.execute(query)
            avg_sdg_data = cursor.fetchall()

              # QUERY 5 AVG SCORE LOWEST
            query = """
            SELECT country_code, AVG(sdg_index_score) as avg_sdg_index
            FROM sdg
            WHERE year BETWEEN 2000 AND 2022
            GROUP BY country_code
            ORDER BY avg_sdg_index ASC
            LIMIT 5;
            """
            cursor.execute(query)
            avg_sdg_data_low = cursor.fetchall()           

            # Query to get the average sdg_index_score per year
            cursor.execute("""
                SELECT year, AVG(sdg_index_score) as avg_score
                FROM sdg
                WHERE year BETWEEN 2000 AND 2022
                GROUP BY year
                ORDER BY year
            """)
            avg_score_by_year_data = cursor.fetchall()

            # Query to get the average goal scores per year
            cursor.execute("""
                SELECT 
                    AVG(goal_1_score) AS avg_goal_1_score,
                    AVG(goal_2_score) AS avg_goal_2_score,
                    AVG(goal_3_score) AS avg_goal_3_score,
                    AVG(goal_4_score) AS avg_goal_4_score,
                    AVG(goal_5_score) AS avg_goal_5_score,
                    AVG(goal_6_score) AS avg_goal_6_score,
                    AVG(goal_7_score) AS avg_goal_7_score,
                    AVG(goal_8_score) AS avg_goal_8_score,
                    AVG(goal_9_score) AS avg_goal_9_score,
                    AVG(goal_10_score) AS avg_goal_10_score,
                    AVG(goal_11_score) AS avg_goal_11_score,
                    AVG(goal_12_score) AS avg_goal_12_score,
                    AVG(goal_13_score) AS avg_goal_13_score,
                    AVG(goal_14_score) AS avg_goal_14_score,
                    AVG(goal_15_score) AS avg_goal_15_score,
                    AVG(goal_16_score) AS avg_goal_16_score,
                    AVG(goal_17_score) AS avg_goal_17_score
                FROM sdg
            """)
            avg_goal_score_by_year_data = cursor.fetchall()

            # Query to get the year with highest goal score
            cursor.execute("""
            SELECT year,
                AVG(goal_1_score) AS avg_goal_1_score,
                AVG(goal_2_score) AS avg_goal_2_score,
                AVG(goal_3_score) AS avg_goal_3_score,
                AVG(goal_4_score) AS avg_goal_4_score,
                AVG(goal_5_score) AS avg_goal_5_score,
                AVG(goal_6_score) AS avg_goal_6_score,
                AVG(goal_7_score) AS avg_goal_7_score,
                AVG(goal_8_score) AS avg_goal_8_score,
                AVG(goal_9_score) AS avg_goal_9_score,
                AVG(goal_10_score) AS avg_goal_10_score,
                AVG(goal_11_score) AS avg_goal_11_score,
                AVG(goal_12_score) AS avg_goal_12_score,
                AVG(goal_13_score) AS avg_goal_13_score,
                AVG(goal_14_score) AS avg_goal_14_score,
                AVG(goal_15_score) AS avg_goal_15_score,
                AVG(goal_16_score) AS avg_goal_16_score,
                AVG(goal_17_score) AS avg_goal_17_score
            FROM sdg
            GROUP BY year
            ORDER BY 
                (AVG(goal_1_score) + AVG(goal_2_score) + AVG(goal_3_score) + AVG(goal_4_score) + AVG(goal_5_score) +
                AVG(goal_6_score) + AVG(goal_7_score) + AVG(goal_8_score) + AVG(goal_9_score) + AVG(goal_10_score) +
                AVG(goal_11_score) + AVG(goal_12_score) + AVG(goal_13_score) + AVG(goal_14_score) + AVG(goal_15_score) +
                AVG(goal_16_score) + AVG(goal_17_score)) / 17 DESC
            LIMIT 1; 
            """)
            highest_goal_year = cursor.fetchall()             

            # Query to get the total count of records in the SDG table
            cursor.execute("SELECT COUNT(*) FROM sdg")
            total_sdg_records = cursor.fetchone()[0]

            # Query to get the total count of records in the Country table
            cursor.execute("SELECT COUNT(*) FROM country")
            total_country_records = cursor.fetchone()[0]

            # Query to get the average sdg_index_score from the SDG table
            cursor.execute("SELECT AVG(sdg_index_score) FROM sdg")
            avg_sdg_index_score = cursor.fetchone()[0]

            # Query to get the total count of records in the Goal table
            cursor.execute("SELECT COUNT(*) FROM goals")
            total_goal_records = cursor.fetchone()[0]

        # Pass all the details to the template as context variables
        context = {
            'user_first_name': user_first_name,
            'user_last_name': user_last_name,
            'user_email': user_email,
            'user_username': user_username,
            'staff_symbol': staff_symbol,
            'total_sdg_records': total_sdg_records,
            'total_country_records': total_country_records,
            'avg_sdg_index_score': avg_sdg_index_score,
            'total_goal_records': total_goal_records,
            'avg_sdg_data': json.dumps(avg_sdg_data),
            'avg_sdg_data_low': json.dumps(avg_sdg_data_low),
            'avg_score_by_year_data': json.dumps(avg_score_by_year_data),
            'avg_goal_score_by_year_data': json.dumps(avg_goal_score_by_year_data),
            'highest_goal_year': json.dumps(highest_goal_year),
        }
        print(avg_score_by_year_data)  # Add this line for debugging
    else:
        messages.success(request, "Please log in to access the dashboard.")
        return redirect('login')  # Redirect to the login page with the message

    return render(request, 'dashboard.html', context)

def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In")
            return redirect('dashboard')
        else:
            messages.success(request, "")
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def login_user(request):
    failed_login = False  # Initialize the failed_login variable
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In")
            return redirect('dashboard')
        else:
            failed_login = True  # Set failed_login to True for a failed attempt
            messages.error(request, "There Was An Error Logging In, Please Try Again")

    return render(request, 'login.html', {'failed_login': failed_login})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered!")
            return redirect('login')  # Redirect to the login page
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

# GOAL PORTION
@login_required
def all_goals(request):
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    query = "SELECT * FROM goals"  
    cursor.execute(query)
    goals = cursor.fetchall()
    goals_data = [
        {
            'id': goal[0],
            'goal_number': goal[1],
            'goal_name': goal[2],
            'goal_description': goal[3]
        }
        for goal in goals
    ]
    cursor.close()
    connection.close()

    context = {'goals': goals_data}
    return render(request, 'all_goals.html', context)

@login_required
def add_goal(request):
    if request.method == 'POST':
        # Get form data
        goal_number = request.POST.get('goal_number')
        goal_name = request.POST.get('goal_name')
        goal_description = request.POST.get('goal_description')

        # Check if the goal_name already exists
        if goal_name_exists(goal_name):
            messages.error(request, f'A goal with the name {goal_name} already exists.')
            return render(request, 'add_goals.html')

        # If goal_name does not exist, proceed with insertion
        mysql_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'vehisenseV2',
        }
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        query = "INSERT INTO goals (goal_number, goal_name, goal_description) VALUES (%s, %s, %s)"
        values = (goal_number, goal_name, goal_description)

        try:
            cursor.execute(query, values)
            connection.commit()
            messages.success(request, 'Goal Added Successfully')
            return redirect('all_goals')
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    return render(request, 'add_goals.html')

def goal_name_exists(goal_name):
    # Check if the goal_name already exists in the database
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM goals WHERE goal_name = %s"
    values = (goal_name,)
    cursor.execute(query, values)
    result = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return result > 0

@login_required
def edit_goal(request, goal_id):
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT * FROM goals WHERE id = %s"
    cursor.execute(query, (goal_id,))
    goal_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if request.method == 'POST':
        goal_number = request.POST.get('goal_number')
        goal_name = request.POST.get('goal_name')
        goal_description = request.POST.get('goal_description')

        # Check if both goal_number and goal_name already exist
        if goal_exists(goal_number, goal_name, goal_id):
            messages.error(request, 'A goal with the same number or name already exists.')
            return render(request, 'edit_goals.html', {'goal_data': goal_data})

        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        update_query = "UPDATE goals SET goal_number = %s, goal_name = %s, goal_description = %s WHERE id = %s"
        update_values = (goal_number, goal_name, goal_description, goal_id)

        try:
            cursor.execute(update_query, update_values)
            connection.commit()
            messages.success(request, 'Goal Updated Successfully')
            return redirect('all_goals')
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    context = {'goal_data': goal_data}
    return render(request, 'edit_goals.html', context)

def goal_exists(goal_number, goal_name, goal_id):
    # Check if the goal_number or goal_name already exist in the database
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM goals WHERE (goal_number = %s OR goal_name = %s) AND id != %s"
    values = (goal_number, goal_name, goal_id)
    cursor.execute(query, values)
    result = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return result > 0

@login_required
def delete_goal(request, goal_id):
    # Connect to MySQL and delete the goal
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    # Delete the goal with the specified goal_id
    delete_query = "DELETE FROM goals WHERE id = %s"
    delete_values = (goal_id,)

    try:
        cursor.execute(delete_query, delete_values)
        connection.commit()
        messages.success(request, 'Goal Deleted Successfully')
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        messages.error(request, 'Error deleting goal')

    cursor.close()
    connection.close()

    return redirect('all_goals')

# COUNTRY PORTION
@login_required
def all_countries(request):
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    query = "SELECT * FROM country"  
    cursor.execute(query)
    country = cursor.fetchall()
    country_data = [
        {
            'id': country[0],
            'country_code': country[1],
            'country_name': country[2],
            'country_description': country[3]
        }
        for country in country
    ]
    cursor.close()
    connection.close()

    context = {'countries': country_data}
    return render(request, 'all_countries.html', context)


@login_required
def add_country(request):
    if request.method == 'POST':
        # Get form data
        country_code = request.POST.get('country_code')
        country_name = request.POST.get('country_name')
        country_description = request.POST.get('country_description')

        # Check if the goal_name already exists
        if country_name_exists(country_name):
            messages.error(request, f'A country with the name {country_name} already exists.')
            return render(request, 'add_country.html')

        # If goal_name does not exist, proceed with insertion
        mysql_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'vehisenseV2',
        }
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        query = "INSERT INTO country (country_code, country_name, country_description) VALUES (%s, %s, %s)"
        values = (country_code, country_name, country_description)

        try:
            cursor.execute(query, values)
            connection.commit()
            messages.success(request, 'Country Added Successfully')
            return redirect('all_countries')
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    return render(request, 'add_country.html')

def country_name_exists(country_name):
    # Check if the goal_name already exists in the database
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM country WHERE country_name = %s"
    values = (country_name,)
    cursor.execute(query, values)
    result = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return result > 0

@login_required
def edit_country(request, country_id):
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT * FROM country WHERE id = %s"
    cursor.execute(query, (country_id,))
    country_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if request.method == 'POST':
        country_code = request.POST.get('country_code')
        country_name = request.POST.get('country_name')
        country_description = request.POST.get('country_description')

        # Check if both goal_number and goal_name already exist
        if country_exists(country_code, country_name, country_id):
            messages.error(request, 'A Country with the same code or name already exists.')
            return render(request, 'edit_country.html', {'country_data': country_data})

        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        update_query = "UPDATE country SET country_code = %s, country_name = %s, country_description = %s WHERE id = %s"
        update_values = (country_code, country_name, country_description, country_id)

        try:
            cursor.execute(update_query, update_values)
            connection.commit()
            messages.success(request, 'Country Updated Successfully')
            return redirect('all_countries')
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    context = {'country_data': country_data}
    return render(request, 'edit_country.html', context)

def country_exists(country_code, country_name, country_id):
    # Check if the goal_number or goal_name already exist in the database
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM country WHERE (country_code = %s OR country_name = %s) AND id != %s"
    values = (country_code, country_name, country_id)
    cursor.execute(query, values)
    result = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return result > 0

@login_required
def delete_country(request, country_id):
    # Connect to MySQL and delete the goal
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    # Delete the goal with the specified goal_id
    delete_query = "DELETE FROM country WHERE id = %s"
    delete_values = (country_id,)

    try:
        cursor.execute(delete_query, delete_values)
        connection.commit()
        messages.success(request, 'Country Deleted Successfully')
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        messages.error(request, 'Error deleting Country')

    cursor.close()
    connection.close()

    return redirect('all_countries')

# COUNTRY PORTION
@login_required
def all_sdg(request):
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    query = "SELECT * FROM sdg"  
    cursor.execute(query)
    sdg = cursor.fetchall()
    sdg_data = [
        {
            'id': sdg[0],
            'country_code': sdg[1],
            'country': sdg[2],
            'year': sdg[3],
            'sdg_index_score': sdg[4],
            'goal_1_score': sdg[5],
            'goal_2_score': sdg[6],
            'goal_3_score': sdg[7],
            'goal_4_score': sdg[8],
            'goal_5_score': sdg[9],
            'goal_6_score': sdg[10],
            'goal_7_score': sdg[11],
            'goal_8_score': sdg[12],
            'goal_9_score': sdg[13],
            'goal_10_score': sdg[14],
            'goal_11_score': sdg[15],
            'goal_12_score': sdg[16],
            'goal_13_score': sdg[17],
            'goal_14_score': sdg[18],
            'goal_15_score': sdg[19],
            'goal_16_score': sdg[20],
            'goal_17_score': sdg[21],
        }
        for sdg in sdg
    ]
    cursor.close()
    connection.close()

    context = {'sdg': sdg_data}
    return render(request, 'all_sdg.html', context)

@login_required
def add_sdg(request):
    # Fetch all countries for populating the <select> elements
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    cursor.execute("SELECT country_code, country_name FROM country")
    countries = cursor.fetchall()

    cursor.close()
    connection.close()

    if request.method == 'POST':
        # Get form data
        country_code = request.POST.get('country_code')
        country = request.POST.get('country')
        year = request.POST.get('year')
        sdg_index_score = request.POST.get('sdg_index_score')
        goal_1_score = request.POST.get('goal_1_score')
        goal_2_score = request.POST.get('goal_2_score')
        goal_3_score = request.POST.get('goal_3_score')
        goal_4_score = request.POST.get('goal_4_score')
        goal_5_score = request.POST.get('goal_5_score')
        goal_6_score = request.POST.get('goal_6_score')
        goal_7_score = request.POST.get('goal_7_score')
        goal_8_score = request.POST.get('goal_8_score')
        goal_9_score = request.POST.get('goal_9_score')
        goal_10_score = request.POST.get('goal_10_score')
        goal_11_score = request.POST.get('goal_11_score')
        goal_12_score = request.POST.get('goal_12_score')
        goal_13_score = request.POST.get('goal_13_score')
        goal_14_score = request.POST.get('goal_14_score')
        goal_15_score = request.POST.get('goal_15_score')
        goal_16_score = request.POST.get('goal_16_score')
        goal_17_score = request.POST.get('goal_17_score')

        # If goal_name does not exist, proceed with insertion
        mysql_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'vehisenseV2',
        }
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        query = "INSERT INTO sdg (country_code, country, year, sdg_index_score, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (country_code, country, year, sdg_index_score, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score)

        try:
            cursor.execute(query, values)
            connection.commit()
            messages.success(request, 'SDG Added Successfully')
            return redirect('all_sdg')
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    # Pass the countries as a list of dictionaries to the template
    country_choices = [{'country_code': code, 'country_name': name} for code, name in countries]
    return render(request, 'add_sdg.html', {'countries': country_choices})


@login_required
def edit_sdg(request, sdg_id):
        # Fetch all countries for populating the <select> elements
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    cursor.execute("SELECT country_code, country_name FROM country")
    countries = cursor.fetchall()

    cursor.close()
    connection.close()

    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT * FROM sdg WHERE id = %s"
    cursor.execute(query, (sdg_id,))
    sdg_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if request.method == 'POST':
        country_code = request.POST.get('country_code')
        country = request.POST.get('country')
        year = request.POST.get('year')
        sdg_index_score = request.POST.get('sdg_index_score')
        goal_1_score = request.POST.get('goal_1_score')
        goal_2_score = request.POST.get('goal_2_score')
        goal_3_score = request.POST.get('goal_3_score')
        goal_4_score = request.POST.get('goal_4_score')
        goal_5_score = request.POST.get('goal_5_score')
        goal_6_score = request.POST.get('goal_6_score')
        goal_7_score = request.POST.get('goal_7_score')
        goal_8_score = request.POST.get('goal_8_score')
        goal_9_score = request.POST.get('goal_9_score')
        goal_10_score = request.POST.get('goal_10_score')
        goal_11_score = request.POST.get('goal_11_score')
        goal_12_score = request.POST.get('goal_12_score')
        goal_13_score = request.POST.get('goal_13_score')
        goal_14_score = request.POST.get('goal_14_score')
        goal_15_score = request.POST.get('goal_15_score')
        goal_16_score = request.POST.get('goal_16_score')
        goal_17_score = request.POST.get('goal_17_score')

        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()


        update_query = "UPDATE sdg SET country_code = %s, country = %s, year = %s, sdg_index_score = %s, goal_1_score = %s, goal_2_score = %s, goal_3_score = %s, goal_4_score = %s, goal_5_score = %s, goal_6_score = %s, goal_7_score = %s, goal_8_score = %s, goal_9_score = %s, goal_10_score = %s, goal_11_score = %s, goal_12_score = %s, goal_13_score = %s, goal_14_score = %s, goal_15_score = %s, goal_16_score = %s, goal_17_score = %s WHERE id = %s"
        update_values = (country_code, country, year, sdg_index_score, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score, sdg_id)

        try:
            cursor.execute(update_query, update_values)
            connection.commit()
            messages.success(request, 'SDG Updated Successfully')
            return redirect('all_sdg')
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    # Pass the countries as a list of dictionaries to the template
    country_choices = [{'country_code': code, 'country': name} for code, name in countries]
    context = {'sdg_data': sdg_data, 'country_choices': country_choices}
    return render(request, 'edit_sdg.html', context)

@login_required
def view_sdg(request, sdg_id):
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    query = "SELECT * FROM sdg WHERE id = %s"
    cursor.execute(query, (sdg_id,))
    sdg_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if request.method == 'POST':
        country_code = request.POST.get('country_code')
        country = request.POST.get('country')
        year = request.POST.get('year')
        sdg_index_score = request.POST.get('sdg_index_score')
        goal_1_score = request.POST.get('goal_1_score')
        goal_2_score = request.POST.get('goal_2_score')
        goal_3_score = request.POST.get('goal_3_score')
        goal_4_score = request.POST.get('goal_4_score')
        goal_5_score = request.POST.get('goal_5_score')
        goal_6_score = request.POST.get('goal_6_score')
        goal_7_score = request.POST.get('goal_7_score')
        goal_8_score = request.POST.get('goal_8_score')
        goal_9_score = request.POST.get('goal_9_score')
        goal_10_score = request.POST.get('goal_10_score')
        goal_11_score = request.POST.get('goal_11_score')
        goal_12_score = request.POST.get('goal_12_score')
        goal_13_score = request.POST.get('goal_13_score')
        goal_14_score = request.POST.get('goal_14_score')
        goal_15_score = request.POST.get('goal_15_score')
        goal_16_score = request.POST.get('goal_16_score')
        goal_17_score = request.POST.get('goal_17_score')

        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()

        update_query = "UPDATE country SET country_code = %s, country = %s, year = %s, sdg_index_score = %s, goal_1_score = %s, goal_2_score = %s, goal_3_score = %s, goal_4_score = %s, goal_5_score = %s, goal_6_score = %s, goal_7_score = %s, goal_8_score = %s, goal_9_score = %s, goal_10_score = %s, goal_11_score = %s, goal_12_score = %s, goal_13_score = %s, goal_14_score = %s, goal_15_score = %s, goal_16_score = %s, goal_17_score = %s WHERE id = %s"
        update_values = (country_code, country, year, sdg_index_score, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score)

        try:
            cursor.execute(update_query, update_values)
            connection.commit()
            messages.success(request, 'SDG Updated Successfully')
            return redirect('all_sdg')
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    context = {'sdg_data': sdg_data}
    return render(request, 'view_sdg.html', context)

@login_required
def delete_sdg(request, sdg_id):
    # Connect to MySQL and delete the goal
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }

    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    # Delete the goal with the specified goal_id
    delete_query = "DELETE FROM sdg WHERE id = %s"
    delete_values = (sdg_id,)

    try:
        cursor.execute(delete_query, delete_values)
        connection.commit()
        messages.success(request, 'SDG Deleted Successfully')
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        messages.error(request, 'Error deleting SDG')

    cursor.close()
    connection.close()

    return redirect('all_sdg')

@login_required
def first_charts(request):
    # Connect to MySQL
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor(dictionary=True)

    # Retrieve SDG data for the year 2022
    query = "SELECT * FROM sdg WHERE year = 2022"
    cursor.execute(query)
    sdg_data = cursor.fetchall()

    # Close MySQL connection
    cursor.close()
    connection.close()

    # Prepare data for Chart.js
    labels = [sdg['country_code'] for sdg in sdg_data]
    sdg_index_scores = [sdg['sdg_index_score'] for sdg in sdg_data]

    context = {
        'labels': json.dumps(labels),
        'sdg_index_scores': json.dumps(sdg_index_scores),
    }
    return render(request, 'first_charts.html', context)

@login_required
def second_charts(request):
# Connect to MySQL
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor(dictionary=True)

    # Retrieve the country with the highest goal_1_score to goal_17_score for the year 2022
    query_highest = (
        "SELECT country_code, country, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, "
        "goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, "
        "goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score "
        "FROM sdg WHERE year = 2022 ORDER BY goal_1_score DESC, goal_2_score DESC, goal_3_score DESC, "
        "goal_4_score DESC, goal_5_score DESC, goal_6_score DESC, goal_7_score DESC, goal_8_score DESC, "
        "goal_9_score DESC, goal_10_score DESC, goal_11_score DESC, goal_12_score DESC, goal_13_score DESC, "
        "goal_14_score DESC, goal_15_score DESC, goal_16_score DESC, goal_17_score DESC LIMIT 1"
    )

    # Retrieve the country with the lowest goal_1_score to goal_17_score for the year 2022
    query_lowest = (
        "SELECT country_code, country, goal_1_score, goal_2_score, goal_3_score, goal_4_score, goal_5_score, "
        "goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, goal_11_score, "
        "goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, goal_17_score "
        "FROM sdg WHERE year = 2022 ORDER BY goal_1_score, goal_2_score, goal_3_score, goal_4_score, "
        "goal_5_score, goal_6_score, goal_7_score, goal_8_score, goal_9_score, goal_10_score, "
        "goal_11_score, goal_12_score, goal_13_score, goal_14_score, goal_15_score, goal_16_score, "
        "goal_17_score LIMIT 1"
    )

    cursor.execute(query_highest)
    highest_data = cursor.fetchone()

    cursor.execute(query_lowest)
    lowest_data = cursor.fetchone()

    # Close MySQL connection
    cursor.close()
    connection.close()

    context = {
        'highest_data': json.dumps(highest_data),
        'lowest_data': json.dumps(lowest_data),
    }
    return render(request, 'second_charts.html', context)

@login_required
def result_2022(request):
    # Connect to MySQL
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'vehisenseV2',
    }
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor(dictionary=True)

    # Initialize dictionaries to store results for each goal
    highest_data = {}
    lowest_data = {}

    for goal_number in range(1, 18):
        # Retrieve the country with the highest goal_score for the specific goal and year
        query_highest = (
            f"SELECT country_code, country, goal_{goal_number}_score "
            f"FROM sdg WHERE year = 2022 ORDER BY goal_{goal_number}_score DESC LIMIT 1"
        )

        # Retrieve the country with the lowest goal_score for the specific goal and year
        query_lowest = (
            f"SELECT country_code, country, goal_{goal_number}_score "
            f"FROM sdg WHERE year = 2022 ORDER BY goal_{goal_number}_score LIMIT 1"
        )

        cursor.execute(query_highest)
        highest_data[goal_number] = cursor.fetchone()

        cursor.execute(query_lowest)
        lowest_data[goal_number] = cursor.fetchone()

    # Close MySQL connection
    cursor.close()
    connection.close()

    context = {
        'highest_data': json.dumps(highest_data),
        'lowest_data': json.dumps(lowest_data),
    }
    return render(request, '2022_result.html', context)








# CSS
# def style(request):
#     return render(request, '')