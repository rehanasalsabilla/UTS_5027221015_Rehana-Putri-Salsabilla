import grpc
from flask import request
from concurrent import futures
import laundry_pb2
import laundry_pb2_grpc
import mysql.connector

class LaundryService(laundry_pb2_grpc.LaundryServiceServicer):
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="insys",
            password="hananaa",
            database="insys_project"
        )
        self.cursor = self.db.cursor()

    def CreateLaundry(self, request, context):
        laundry = request.laundry
        sql = "INSERT INTO laundry (customer_name, address, pickup_date, delivery_date, status) VALUES (%s, %s, %s, %s, %s)"
        values = (laundry.customer_name, laundry.address, laundry.pickup_date, laundry.delivery_date, laundry.status)
        self.cursor.execute(sql, values)
        self.db.commit()
        return laundry_pb2.CreateResponse(message="Laundry created successfully.")

    def ReadLaundry(self, request, context):
        id = request.id
        if id:
            sql = "SELECT * FROM laundry WHERE id = %s"
            self.cursor.execute(sql, (id,))
        else:
            sql = "SELECT * FROM laundry"
            self.cursor.execute(sql)
        
        result = self.cursor.fetchall()
        laundry_list = []
        for row in result:
            laundry = laundry_pb2.Laundry(
                id=row[0],
                customer_name=row[1],
                address=row[2],
                pickup_date=row[3],
                delivery_date=row[4],
                status=row[5]
            )
            laundry_list.append(laundry)
        return laundry_pb2.ReadResponse(laundry=laundry_list)

    def UpdateLaundry(self, request, context):
        laundry = request.laundry
        sql = "UPDATE laundry SET customer_name = %s, address = %s, pickup_date = %s, delivery_date = %s, status = %s WHERE id = %s"
        values = (laundry.customer_name, laundry.address, laundry.pickup_date, laundry.delivery_date, laundry.status, laundry.id)
        self.cursor.execute(sql, values)
        self.db.commit()
        return laundry_pb2.UpdateResponse(message="Laundry updated successfully.")

    def DeleteLaundry(self, request, context):
        id = request.id
        sql = "DELETE FROM laundry WHERE id = %s"
        self.cursor.execute(sql, (id,))
        self.db.commit()
        return laundry_pb2.DeleteResponse(message="Laundry deleted successfully.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    laundry_pb2_grpc.add_LaundryServiceServicer_to_server(LaundryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
