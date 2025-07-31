
@app.route('/add_vehicle', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if request.method == 'GET':
        return render_template('add_vehicle.html')
        
    elif request.method == 'POST':
        connection = None
        cursor = None
        try:
            # Get form data
            vehicle_no = request.form.get('vehicle_no')
            vehicle_model = request.form.get('vehicle_model')
            seats_available = request.form.get('seats_available')
            
            # Validate form data
            if not all([vehicle_no, vehicle_model, seats_available]):
                flash('Please fill in all fields', 'error')
                return redirect(url_for('add_vehicle'))
                
            # Convert seats_available to integer
            try:
                seats_available = int(seats_available)
                if seats_available <= 0:
                    flash('Number of seats must be greater than 0', 'error')
                    return redirect(url_for('add_vehicle'))
            except ValueError:
                flash('Invalid number of seats', 'error')
                return redirect(url_for('add_vehicle'))
            
            # Get database connection
            connection = get_db_connection()
            if not connection:
                flash('Database connection failed', 'error')
                return redirect(url_for('add_vehicle'))
                
            cursor = connection.cursor()
            
            # Check if vehicle number already exists
            cursor.execute('SELECT vehicle_id FROM vehicle WHERE vehicle_no = %s', (vehicle_no,))
            if cursor.fetchone():
                flash('Vehicle with this number already exists', 'error')
                return redirect(url_for('add_vehicle'))