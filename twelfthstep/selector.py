import click
from tabulate import tabulate

from twelfthstep.connector import connect


@click.group()
def main():
    pass


@main.command()
def read():
    """ Lists all topics in the database """
    dbx = connect
    topic_inv_count = dbx("SELECT COUNT(*) FROM Topics")
    topic_inv_count = topic_inv_count.rows[0][0]
    if topic_inv_count is 0:
        print("there are no topics defined within the database")
    else:
        dx = dbx("SELECT TID, Topic, Description FROM Topics ORDER BY TID")
        print("\nMEETING STARTER TOPICS\n")
        click.secho(tabulate(dx.rows, headers=["TID", "Topic", "Desc."]), fg="bright_green")
        print("")


@main.command()
@click.argument("count", type=int, nargs=1)
def select(count):
    """ Selects a number of topics equal to [COUNT] """
    dbx = connect
    topic_inv_count = dbx("SELECT COUNT(*) FROM Topics")
    topic_inv_count = topic_inv_count.rows[0][0]
    if count is 0:
        print("there are no topics defined within the database")
    if count > topic_inv_count:
        print("requested number exceeds # of available topics")
    else:
        sql = "SELECT Topic, Description FROM Topics ORDER BY RANDOM() LIMIT ?"
        dx = dbx(sql, (count,))
        print("\nMEETING STARTER TOPICS\n")
        click.secho(tabulate(dx.rows, headers=["Topic", "Desc."]), fg="bright_green")
        print("")


if __name__ == "__main__":
    main()
