from flask import Flask, render_template, request, redirect, url_for
import grpc
import laundry_pb2
import laundry_pb2_grpc

app = Flask(__name__)

# Fungsi untuk membuat koneksi ke gRPC server
def create_stub():
    channel = grpc.insecure_channel('localhost:50051')
    return laundry_pb2_grpc.LaundryServiceStub(channel)

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman Create Laundry
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        stub = create_stub()
        customer_name = request.form['customer_name']
        address = request.form['address']
        pickup_date = request.form['pickup_date']
        delivery_date = request.form['delivery_date']
        status = request.form['status']
        laundry = laundry_pb2.Laundry(
            customer_name=customer_name,
            address=address,
            pickup_date=pickup_date,
            delivery_date=delivery_date,
            status=status
        )
        response = stub.CreateLaundry(laundry_pb2.CreateRequest(laundry=laundry))
        return redirect(url_for('index'))
    return render_template('create_laundry.html')

# Route untuk halaman Read Laundry Form
@app.route('/read', methods=['GET'])
def read_form():
    return render_template('read_laundry.html')


# Route untuk halaman Read by ID
@app.route('/read_by_id', methods=['GET', 'POST'])
def read_by_id():
    if request.method == 'POST':
        stub = create_stub()
        laundry_id = int(request.form['laundry_id'])
        response = stub.ReadLaundry(laundry_pb2.ReadRequest(id=laundry_id))
        return render_template('read_by_id.html', laundry=response.laundry)
    return render_template('read_laundry.html')


# Route untuk halaman Update Laundry
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        stub = create_stub()
        laundry_id = int(request.form['laundry_id'])
        customer_name = request.form['customer_name']
        address = request.form['address']
        pickup_date = request.form['pickup_date']
        delivery_date = request.form['delivery_date']
        status = request.form['status']
        updated_laundry = laundry_pb2.Laundry(
            id=laundry_id,
            customer_name=customer_name,
            address=address,
            pickup_date=pickup_date,
            delivery_date=delivery_date,
            status=status
        )
        response = stub.UpdateLaundry(laundry_pb2.UpdateRequest(laundry=updated_laundry))
        return redirect(url_for('index'))
    return render_template('update_laundry.html')

# Route untuk halaman Delete Laundry
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        stub = create_stub()
        laundry_id = int(request.form['laundry_id'])
        response = stub.DeleteLaundry(laundry_pb2.DeleteRequest(id=laundry_id))
        return redirect(url_for('index'))
    return render_template('delete_laundry.html')

if __name__ == '__main__':
    app.run(debug=True)
