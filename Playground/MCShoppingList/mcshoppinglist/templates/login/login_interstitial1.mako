<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8"/>
    <title>MC Shopping List : Login</title>
  </head>
  <body>
    <h1>MC Shopping List : Please Login</h1>
    <div>
        <a href="#"><img alt="Login with Facebook" src="${static_content_path}/images/login/login-facebook.png"/></a>
        <a href="#"><img alt="Login with Google" src="${static_content_path}/images/login/login-google.png"/></a>
    </div>
    <div>
        <form novalidate method="POST" action="">
            <div>
                <p>Username:</p>
                <input type="text" name="username" autofocus required/>
            </div>
            <div>
                <p>Password:</p>
                <input type="password" name="password" required/>
            </div>
            <div>
                <input type="submit" value="Sign In"/>
            </div>
        </form>
    </div>
    <div>
        <p><a href="signup/">Create a new account.</a></p>
    </div>
  </body>
</html>