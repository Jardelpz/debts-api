from app import app
import routes.person
import model.person
import routes.debt
import model.debt


if __name__ == '__main__':
    app.run(debug=True, port=8000)

