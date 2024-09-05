# HOW TO RUN DEMO

## Prerequisites
- Ensure you have Dapr installed on your machine.
- Make sure MySQL is installed and running, with a database ready to connect.
- Create python enviroment

## Steps to Run

### 1. Update the MySQL Connection String
Before running the demo, modify the MySQL connection string in the component configuration file. Replace `<user>`, `<password>`, `<host>`, and `<database>` with your actual database credentials:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: my-mysql
spec:
  type: bindings.mysql
  version: v1
  metadata:
    - name: url  # Required, define DB connection in DSN format
      value: "<user>:<password>@tcp(<host:port>)/<database>"

```

## Execute
Navigate to the application directory, then run the following command. This will start the application using Dapr:

```bash
dapr run --app-id usersapp --app-port 5000 --dapr-http-port 3500 --components-path ./components  python ./src/http/app.py
```
