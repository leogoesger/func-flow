python3 -m virtualenv env
source env/bin/activate
pip freeze > requirements.txt
pip install -r requirements.txt
deactivate

# gutsy-client

## About

This project uses [Python3](https://www.python.org/)

## Getting Started In 1, 2 and 3

1. Install [Python3](https://www.python.org/downloads/)
2. Create `dev` and `test` database in Postgres

   ```
   psql;
   CREATE DATABASE gutsy_development;
   CREATE DATABASE gutsy_test;
   ```

3. Install your dependencies

   ```
   cd path/to/gutsy-api; yarn
   ```

4. Start your app

   ```
   yarn start
   ```

## Testing

Simply run `yarn test` and all your tests in the `test/` directory will be run.

## CI

It uses [Travis-CI](https://travis-ci.org/) and [Coveralls](https://coveralls.io/).

## Sequelize CLI

```
$ npm install -g sequelize-cli

$ sequelize model:create --name TodoItem --attributes content:string,complete:boolean #Generate a model
```

## Help

For more information on all the things you can do with Sequelize CLI visit [sequelize cli ](https://github.com/sequelize/cli).

## Scripts

```
"test": "NODE_ENV=test yarn run test-prepare ; NODE_ENV=test npm run mocha", # Clear database before all the tests are run
"test-cover": "NODE_ENV=test nyc --reporter=text npm run mocha",             # Generate test coverage report locally
"test-coverage": "nyc report --reporter=text-lcov | coveralls",              # Generate test coverage and send it to Coveralls
```

## Options

[Postico](https://eggerapps.at/postico/): A Modern PostgreSQL Client for the Mac

## License

Copyright (c) 2017

Licensed under the [MIT license](LICENSE).
