
# isolate logic of method returning messages
# rendering in routes file

# having method to unit test in isolation without having to respond to requests, have the server running or flash method

class NewUserError(Exception):
    pass

def create_user(user):

    if not user.username:
        raise NewUserError("Username already taken. Please try another!")
    
    if not user.email:
        raise NewUserError("Email already registerd. Please Login")



# in routes
# catch error once and flash error

# try:
#     new_user(user)

# except NewUserError as e:
#     flash(e.message, 'error')
#     return render_template(...)

# return redirect(...)