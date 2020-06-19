from app import app
import routes.person
import model.person


if __name__ == '__main__':
    app.run(debug=True, port=8000)

