<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8"/>
    <title>MC Shopping List : Sign Up</title>
  </head>
  <body>
    <h1>MC Shopping List : Sign Up</h1>
    <form novalidate method="POST" action="">
        <div>
            <p>Choose a username:</p>
            <input type="text" name="username" autofocus required/>
        </div>
        <div>
            <p>Enter your email address:</p>
            <input type="text" name="email" required/>
        </div>
        <div>
            <p>Enter a password:</p>
            <input type="password" name="password" required/>
        </div>
        <div>
            <p>Confirm your password:</p>
            <input type="password" name="confirmPassword" required/>
        </div>
        <div>
            <p>Enter the text below:</p>
            <p>(CAPTCHA placeholder.)</p>
        </div>
        <div>
            <input type="submit" value="Sign In"/>
        </div>
    </form>
    <div>
        <p>Already have an account? <a href="../../login/">Login here.</a></p>
    </div>
  </body>
</html>