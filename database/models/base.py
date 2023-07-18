import peewee
import settings

psql_database = peewee.PostgresqlDatabase(settings.DATABASE_NAME,
                                          user=settings.USER_NAME,
                                          password=settings.PASSWORD,
                                          host=settings.HOST,
                                          port=settings.PORT)


def table_name(model_class):
    model_name = model_class.__name__
    return model_name.lower() + '_table'


class DefaultDatabaseModel(peewee.Model):
    class Meta:
        database = psql_database
        table_function = table_name 