 # Verify the hashed password
                session["adlogin"] = True
                session["email"] = email  # Store email instead of username
                flash("Admin logged in Successfully", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid Admin email or password!", "danger")
                return redirect(url_for('adlogin'))
        finally:
            con.close()
