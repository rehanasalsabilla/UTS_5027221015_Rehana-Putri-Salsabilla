import grpc
import laundry_pb2
import laundry_pb2_grpc

def create_laundry(stub):
    customer_name = input("Masukkan nama pelanggan: ")
    address = input("Masukkan alamat pelanggan: ")
    pickup_date = input("Masukkan tanggal pengambilan (YYYY-MM-DD): ")
    delivery_date = input("Masukkan tanggal pengiriman (YYYY-MM-DD): ")
    status = input("Masukkan status laundry: ")

    laundry = laundry_pb2.Laundry(
        customer_name=customer_name,
        address=address,
        pickup_date=pickup_date,
        delivery_date=delivery_date,
        status=status
    )
    response = stub.CreateLaundry(laundry_pb2.CreateRequest(laundry=laundry))
    print(response.message)

def read_laundry(stub):
    laundry_id = int(input("Masukkan ID laundry yang ingin dibaca: "))
    response = stub.ReadLaundry(laundry_pb2.ReadRequest(id=laundry_id))
    print(response.laundry)

def update_laundry(stub):
    laundry_id = int(input("Masukkan ID laundry yang ingin diupdate: "))
    customer_name = input("Masukkan nama pelanggan baru: ")
    address = input("Masukkan alamat baru: ")
    pickup_date = input("Masukkan tanggal pengambilan baru (YYYY-MM-DD): ")
    delivery_date = input("Masukkan tanggal pengiriman baru (YYYY-MM-DD): ")
    status = input("Masukkan status baru: ")

    updated_laundry = laundry_pb2.Laundry(
        id=laundry_id,
        customer_name=customer_name,
        address=address,
        pickup_date=pickup_date,
        delivery_date=delivery_date,
        status=status
    )
    response = stub.UpdateLaundry(laundry_pb2.UpdateRequest(laundry=updated_laundry))
    print(response.message)

def delete_laundry(stub):
    laundry_id = int(input("Masukkan ID laundry yang ingin dihapus: "))
    response = stub.DeleteLaundry(laundry_pb2.DeleteRequest(id=laundry_id))
    print(response.message)

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = laundry_pb2_grpc.LaundryServiceStub(channel)

    while True:
        print("\nPilih operasi yang ingin Anda lakukan:")
        print("1. Create Laundry")
        print("2. Read Laundry")
        print("3. Update Laundry")
        print("4. Delete Laundry")
        print("5. Keluar")

        choice = input("Masukkan nomor pilihan: ")

        if choice == "1":
            create_laundry(stub)
        elif choice == "2":
            read_laundry(stub)
        elif choice == "3":
            update_laundry(stub)
        elif choice == "4":
            delete_laundry(stub)
        elif choice == "5":
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == '__main__':
    run()
