from cx_Oracle import *
class model:
    def __init__(self):
        self.song_dict={}
        self.db_status=True
        self.conn=None
        self.cur=None
        try:
            self.conn=connect("mouzikka/music@LAPTOP-PGTJ8HE0/orcl")
            print("connected successfully to db")
            self.cur=self.conn.cursor()
        except DatabaseError:
            self.db_status=False
    def get_db_status(self):
        return self.db_status
    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("cursor close successfully")
        if self.conn is not None:
            self.conn.close()
            print("Disconnected successfully from the DB")
    def add_song(self,song_name,song_path):
        self.song_dict[song_name]=song_path
        print("song added",self.song_dict[song_name])
    def get_song_path(self,song_name):
        return self.song_dict[song_name]
    def remove_song(self,song_name):
        self.song_dict.pop(song_name)
        print(self.song_dict)
    def search_song_in_favourites(self,song_name):
        self.cur.execute("select song_name from MYFAVOURITES where song_name=:1",(song_name,))
        song_tuple=self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True

    def add_song_to_favourites(self,song_name,song_path):
        is_song_present=self.search_song_in_favourites(song_name)
        if is_song_present:
            return "song already present in your favourites"
        self.cur.execute("select max(song_id) from MYFAVOURITES")
        last_song_id=self.cur.fetchone()[0]
        next_song_id=1
        if last_song_id is not None:
            next_song_id=last_song_id+1
        self.cur.execute("insert into MYFAVOURITES values(:1,:2,:3)",(next_song_id,song_name,song_path))
        self.conn.commit()
        return "song added to your favourites"

    def remove_song_from_favourites(self, song_name):
        is_song_present=self.search_song_in_favourites(song_name)
        if is_song_present:
            self.cur.execute("delete from myfavourites where song_name=:1",(song_name,))
            #self.cur.execute(f"delete from myfavourites where song_name='{song_name}'")
            self.conn.commit()
            return ("song removed from your favourites")
        else:
            return ("song not present in your favourites")
        #self.cur.execute("delete from myfavourites where song_name=:1",(song_name,))
        #self.conn.commit()
        #m=1 format
        #m=self.cur.rowcount
        #if m!=0:
            ##self.song_dict.pop(song_name)
            #return ("song removed from your favourites")
        #else:
            #return ("song not present in your favourites")

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from MYFAVOURITES")
        songs_present=False
        for song_name,song_path in self.cur:
            self.song_dict[song_name]=song_path
            songs_present=True
        if songs_present==True:
            return "List populated from favourites"
        else:
            return "no song present in your favourites"
