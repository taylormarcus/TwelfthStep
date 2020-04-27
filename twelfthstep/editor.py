import click

from twelfthstep.connector import connect


def done(message: str):
    click.secho("success: {}".format(message), fg="bright_green")


def fail(message: str):
    click.secho("error: {}".format(message), fg="red")
    exit()


def editor(**kwargs):
    dbx = connect
    sql = None
    data_params = None

    # Create
    if "delete_id" and "update_id" not in kwargs:
        sql = "INSERT INTO Topics ('Topic', 'Description') VALUES(?, ?)"
        data_params = tuple(kwargs.values())
    # Update
    elif "update_id" in kwargs:
        # Update whole topic
        if all(k in kwargs for k in ("description", "topic", "update_id")):
            sql = "UPDATE Topics SET Topic=?, Description=? WHERE TID=?"
            data_params = tuple(kwargs.values())
        # Update description
        elif all(k in kwargs for k in ("description", "update_id")):
            sql = "UPDATE Topics SET Description=? WHERE TID=?"
            data_params = tuple(kwargs.values())
        # Update topic
        elif all(k in kwargs for k in ("topic", "update_id")):
            sql = "UPDATE Topics SET Topic=:topic WHERE TID=:update_id"
            data_params = tuple(kwargs.values())
    # Delete
    elif "delete_id" in kwargs:
        sql = "DELETE FROM Topics WHERE TID=?"
        data_params = (kwargs.get("delete_id"),)

    return dbx(sql, data_params)


@click.group()
def main():
    pass


@main.command()
@click.argument("topic", type=str, nargs=1)
@click.argument("description", type=str, nargs=1)
def create(topic, description):
    """ Creates a new topic [TOPIC] [DESCRIPTION]"""
    e = editor(topic=topic, description=description)
    if e.affected_rows is 1:
        done("topic '{}' added successfully".format(topic))
    else:
        fail("topic '{}' could not be added".format(topic))


@main.command()
@click.argument("tid", type=int, nargs=1)
@click.argument("topic", type=str, nargs=1)
@click.argument("description", type=str, nargs=1)
def update(topic, description, tid):
    """ Updates a topic [TID] [TOPIC] [DESCRIPTION] """
    e = editor(topic=topic, description=description, update_id=tid)
    if e.affected_rows is 1:
        done("topic '{}' was updated successfully".format(topic))
    else:
        fail("topic not updated")


@main.command()
@click.argument("tid", type=int, nargs=1)
@click.argument("description", type=str, nargs=1)
def update_description(description, tid):
    """ Updates a topic [TID] [DESCRIPTION] """
    e = editor(description=description, update_id=tid)
    if e.affected_rows is 1:
        done("topic description updated successfully")
    else:
        fail("topic description not updated")


@main.command()
@click.argument("tid", type=int, nargs=1)
@click.argument("topic", type=str, nargs=1)
def update_topic(topic, tid):
    """ Updates a topic [TID] [TOPIC] """
    e = editor(topic=topic, update_id=tid)
    if e.affected_rows is 1:
        done("topic '{}' was updated successfully".format(topic))
    else:
        fail("topic title not updated")


@main.command()
@click.argument("tid", type=int, nargs=-1)
def delete(tid: int) -> None:
    """ Deletes a topic by [TID] """
    e = None
    if isinstance(tid, tuple):
        for _id in tid:
            e = editor(delete_id=_id)
    else:
        e = editor(delete_id=tid)
    if e.affected_rows is 1:
        done("topic id '{}' deleted successfully".format(tid))
    else:
        fail("topic id '{}' was not deleted".format(tid))


if __name__ == "__main__":
    main()
