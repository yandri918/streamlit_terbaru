
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Helper for custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono&display=swap');
        
        * { font-family: 'Inter', sans-serif; }
        code, pre { font-family: 'JetBrains Mono', monospace !important; }
        
        .course-header {
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
            color: white; padding: 2.5rem; border-radius: 20px;
            margin-bottom: 2rem; text-align: center;
        }
        .course-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; }
        
        .theory-box {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 5px solid #3b82f6; padding: 1.5rem;
            border-radius: 12px; margin: 1rem 0;
        }
        .example-box {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-left: 5px solid #10b981; padding: 1.5rem;
            border-radius: 12px; margin: 1rem 0;
        }
        .theorem-box {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 5px solid #f59e0b; padding: 1.5rem;
            border-radius: 12px; margin: 1rem 0;
        }
        .definition {
            background: #faf5ff; border-left: 4px solid #8b5cf6;
            padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

def render_ma101_simulation():
    """Interactive Simulation for Calculus (Limits & Derivatives)"""
    st.markdown("### 🧮 Interactive Limit Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        a_val = st.number_input("Approach value (a)", value=2.0, step=0.1)
    with col2:
        func_type = st.selectbox("Function type", ["Polynomial", "Rational", "Exponential"])
    
    # Generate data for limit visualization
    x_vals = np.linspace(a_val - 2, a_val + 2, 100)
    
    if func_type == "Polynomial":
        y_vals = x_vals**2 + 3*x_vals - 1
        limit_val = a_val**2 + 3*a_val - 1
    elif func_type == "Rational":
        y_vals = (x_vals**2 - 4) / (x_vals - 2) if a_val == 2 else x_vals**2 / x_vals
        limit_val = 4 if a_val == 2 else a_val
    else:  # Exponential
        y_vals = np.exp(x_vals)
        limit_val = np.exp(a_val)
    
    df_limit = pd.DataFrame({'x': x_vals, 'y': y_vals})
    
    # Altair chart
    line = alt.Chart(df_limit).mark_line(color='#3b82f6', strokeWidth=3).encode(
        x=alt.X('x:Q', title='x'),
        y=alt.Y('y:Q', title='f(x)'),
        tooltip=['x', 'y']
    )
    
    st.altair_chart(line, use_container_width=True)
    st.info(f"📊 The limit as x → {a_val} is approximately **{limit_val:.2f}**")

def render_ma102_simulation():
    """Interactive Matrix Calculator for Linear Algebra"""
    st.markdown("### 🧮 2×2 Matrix Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Matrix A:**")
        a11 = st.number_input("a₁₁", -10.0, 10.0, 2.0, 0.5, key="a11")
        a12 = st.number_input("a₁₂", -10.0, 10.0, 1.0, 0.5, key="a12")
        a21 = st.number_input("a₂₁", -10.0, 10.0, 3.0, 0.5, key="a21")
        a22 = st.number_input("a₂₂", -10.0, 10.0, 4.0, 0.5, key="a22")
    
    with col2:
        st.markdown("**Matrix B:**")
        b11 = st.number_input("b₁₁", -10.0, 10.0, 1.0, 0.5, key="b11")
        b12 = st.number_input("b₁₂", -10.0, 10.0, 0.0, 0.5, key="b12")
        b21 = st.number_input("b₂₁", -10.0, 10.0, 0.0, 0.5, key="b21")
        b22 = st.number_input("b₂₂", -10.0, 10.0, 1.0, 0.5, key="b22")
    
    A = np.array([[a11, a12], [a21, a22]])
    B = np.array([[b11, b12], [b21, b22]])
    
    # Calculate operations
    A_plus_B = A + B
    AB = A @ B
    det_A = np.linalg.det(A)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**A + B:**")
        st.code(f"[{A_plus_B[0,0]:.1f}  {A_plus_B[0,1]:.1f}]\n[{A_plus_B[1,0]:.1f}  {A_plus_B[1,1]:.1f}]")
    with col2:
        st.markdown("**AB:**")
        st.code(f"[{AB[0,0]:.1f}  {AB[0,1]:.1f}]\n[{AB[1,0]:.1f}  {AB[1,1]:.1f}]")
    with col3:
        st.metric("det(A)", f"{det_A:.2f}")

def render_ce101_simulation():
    """Interactive Simulation for Programming (CE101)"""
    st.markdown("### 💻 Code Playground")
    st.markdown("Experiment with basic Python structures directly in your browser.")

    code_template = st.selectbox("Select a template:", 
        ["Hello World", "For Loop", "If-Else", "Function Definition"])
    
    default_code = ""
    if code_template == "Hello World":
        default_code = 'print("Hello, UTel University!")'
    elif code_template == "For Loop":
        default_code = 'for i in range(5):\n    print(f"Iteration {i}")'
    elif code_template == "If-Else":
        default_code = 'x = 10\nif x > 5:\n    print("x is greater than 5")\nelse:\n    print("x is small")'
    else:
        default_code = 'def greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("Student"))'

    code_input = st.text_area("Write your Python code here:", value=default_code, height=150)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("▶️ Run Code"):
            st.markdown("**Output:**")
            try:
                # Capture stdout
                import sys
                from io import StringIO
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()
                
                exec(code_input, {})
                
                sys.stdout = old_stdout
                st.code(redirected_output.getvalue())
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        st.info("💡 Tip: Use `print()` to see output.")

def render_ph101_simulation():
    """Interactive Simulation for Physics (PH101)"""
    st.markdown("### 🧪 Harmonic Oscillator Simulation")
    
    col1, col2 = st.columns(2)
    with col1:
        amplitude = st.slider("Amplitude (A)", 0.1, 5.0, 1.0, 0.1)
        frequency = st.slider("Frequency (f)", 0.1, 5.0, 1.0, 0.1)
    with col2:
        phase = st.slider("Phase (φ)", 0.0, 2*np.pi, 0.0, 0.1)
        damping = st.slider("Damping (ζ)", 0.0, 1.0, 0.0, 0.05)
        
    t = np.linspace(0, 10, 500)
    # y = A * exp(-ζt) * cos(2πft + φ)
    y = amplitude * np.exp(-damping * t) * np.cos(2 * np.pi * frequency * t + phase)
    
    df_oscillator = pd.DataFrame({'Time (s)': t, 'Displacement (m)': y})
    
    chart = alt.Chart(df_oscillator).mark_line(color='#ef4444', strokeWidth=2).encode(
        x='Time (s)',
        y='Displacement (m)',
        tooltip=['Time (s)', 'Displacement (m)']
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    # Calculate energy
    k = 10  # Spring constant (assumed)
    m = k / (2 * np.pi * frequency)**2
    potential_energy = 0.5 * k * y**2
    # Velocity v = dy/dt
    # y' = A * [ -ζ * exp(-ζt) * cos(2πft + φ) - exp(-ζt) * 2πf * sin(2πft + φ) ]
    # y' = -A * exp(-ζt) * [ ζ * cos(...) + 2πf * sin(...) ]
    velocity = -amplitude * np.exp(-damping*t) * (damping * np.cos(2*np.pi*frequency*t + phase) + 2*np.pi*frequency * np.sin(2*np.pi*frequency*t + phase))
    kinetic_energy = 0.5 * m * velocity**2
    
    st.info(f"System Properties: Mass = {m:.2f} kg, Spring Constant = {k} N/m")

def render_ce302_simulation():
    """Interactive Simulation for Digital Systems (CE302)"""
    st.markdown("### ⚡ Logic Gate Simulator")
    
    col1, col2 = st.columns(2)
    with col1:
        gate_type = st.selectbox("Select Gate", ["AND", "OR", "NOT", "NAND", "NOR", "XOR"])
    with col2:
        input_a = st.checkbox("Input A", value=False)
        input_b = st.checkbox("Input B", value=False) if gate_type != "NOT" else False
        
    result = False
    if gate_type == "AND":
        result = input_a and input_b
    elif gate_type == "OR":
        result = input_a or input_b
    elif gate_type == "NOT":
        result = not input_a
    elif gate_type == "NAND":
        result = not (input_a and input_b)
    elif gate_type == "NOR":
        result = not (input_a or input_b)
    elif gate_type == "XOR":
        result = input_a != input_b
        
    st.markdown("---")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.metric("Input A", "1" if input_a else "0")
    with c2:
        if gate_type != "NOT":
            st.metric("Input B", "1" if input_b else "0")
    with c3:
        st.metric("Output", "1" if result else "0", delta="High" if result else "Low")
        
    # Truth Table
    st.markdown("#### Truth Table")
    if gate_type == "NOT":
        df = pd.DataFrame({'A': [0, 1], 'Output': [1, 0]})
    else:
        # Generate truth table for 2 inputs
        inputs = [(0,0), (0,1), (1,0), (1,1)]
        outputs = []
        for a, b in inputs:
            if gate_type == "AND": out = a and b
            elif gate_type == "OR": out = a or b
            elif gate_type == "NAND": out = not (a and b)
            elif gate_type == "NOR": out = not (a or b)
            elif gate_type == "XOR": out = a != b
            outputs.append(int(out))
            
        df = pd.DataFrame({
            'A': [i[0] for i in inputs],
            'B': [i[1] for i in inputs],
            'Output': outputs
        })
    
    # Highlight current state
    def highlight_row(row):
        is_active = False
        if gate_type == "NOT":
            is_active = (row['A'] == int(input_a))
        else:
            is_active = (row['A'] == int(input_a)) and (row['B'] == int(input_b))
        return ['background-color: #dbeafe' if is_active else '' for _ in row]

    st.dataframe(df.style.apply(highlight_row, axis=1), use_container_width=True)

def render_ce103_simulation():
    """Interactive Simulation for Computer Architecture (CE103)"""
    st.markdown("### 🖥️ Simple ALU & Number Systems")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Input A**")
        val_a = st.number_input("Decimal Value A", value=10, step=1)
        bin_a = format(val_a & 0xFF, '08b')
        hex_a = format(val_a & 0xFF, '02X')
        st.code(f"BIN: {bin_a}\nHEX: 0x{hex_a}")
        
    with col2:
        st.markdown("**Input B**")
        val_b = st.number_input("Decimal Value B", value=6, step=1)
        bin_b = format(val_b & 0xFF, '08b')
        hex_b = format(val_b & 0xFF, '02X')
        st.code(f"BIN: {bin_b}\nHEX: 0x{hex_b}")

    st.markdown("---")
    st.markdown("**ALU Operation**")
    op = st.selectbox("Operation", ["ADD", "SUB", "AND", "OR", "XOR", "LSHIFT", "RSHIFT"])
    
    res = 0
    if op == "ADD": res = val_a + val_b
    elif op == "SUB": res = val_a - val_b
    elif op == "AND": res = val_a & val_b
    elif op == "OR": res = val_a | val_b
    elif op == "XOR": res = val_a ^ val_b
    elif op == "LSHIFT": res = val_a << 1
    elif op == "RSHIFT": res = val_a >> 1
    
    # Mask to 8-bit for visualization simplicity
    res_8bit = res & 0xFF
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Result (Dec)", res)
    c2.metric("Result (Bin)", format(res_8bit, '08b'))
    c3.metric("Result (Hex)", f"0x{format(res_8bit, '02X')}")
    
    # Visual Bits
    st.caption("8-bit Visualization:")
    bits = [int(x) for x in format(res_8bit, '08b')]
    cols = st.columns(8)
    for i, bit in enumerate(bits):
        cols[i].button(str(bit), key=f"bit_{i}", disabled=True, type="primary" if bit else "secondary")

def render_ee101_simulation():
    """Interactive Simulation for Electronics (EE101)"""
    st.markdown("### ⚡ Circuit Simulator (Ohm's Law)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Parameters")
        voltage = st.slider("Voltage (V)", 0.0, 24.0, 5.0, 0.5)
        resistance = st.slider("Resistance (Ω)", 10.0, 1000.0, 100.0, 10.0)
        
        current = voltage / resistance * 1000 # mA
        power = (voltage ** 2) / resistance # Watts
        
        st.markdown("#### Calculations")
        st.metric("Current (I)", f"{current:.1f} mA")
        st.metric("Power (P)", f"{power:.3f} W")
        
    with col2:
        st.markdown("#### V-I Characteristic Plot")
        # Generate VI curve for fixed R
        v_range = np.linspace(0, 24, 100)
        i_vals = (v_range / resistance) * 1000 # mA
        
        df_vi = pd.DataFrame({'Voltage (V)': v_range, 'Current (mA)': i_vals})
        
        # Point for current state
        curr_point = pd.DataFrame({'Voltage (V)': [voltage], 'Current (mA)': [current]})
        
        base = alt.Chart(df_vi).mark_line().encode(x='Voltage (V)', y='Current (mA)')
        point = alt.Chart(curr_point).mark_point(color='red', size=100, filled=True).encode(
            x='Voltage (V)', y='Current (mA)', tooltip=['Voltage (V)', 'Current (mA)']
        )
        
        st.altair_chart(base + point, use_container_width=True)
        
        st.info("Ohm's Law: $V = I \\cdot R$")

def render_ce201_simulation():
    """Interactive Simulation for OOP (CE201)"""
    st.markdown("### 🧬 Object-Oriented Designer")
    
    st.markdown("#### Class Definition: `Car`")
    col1, col2 = st.columns(2)
    with col1:
        color = st.selectbox("Color", ["Red", "Blue", "Black", "White"])
        model = st.text_input("Model", "Tesla Model 3")
    with col2:
        speed = st.slider("Max Speed (km/h)", 100, 300, 200)
        is_electric = st.checkbox("Is Electric?", value=True)
        
    st.markdown("#### Object Instantiation")
    if st.button("Create Object"):
        st.code(f"""
class Car:
    def __init__(self, color, model, speed, is_electric):
        self.color = "{color}"
        self.model = "{model}"
        self.max_speed = {speed}
        self.is_electric = {is_electric}

    def drive(self):
        return f"Driving the {color} {model} at {speed} km/h!"

# Object
my_car = Car("{color}", "{model}", {speed}, {is_electric})
print(my_car.drive())
        """, language="python")
        st.success(f"Output: Driving the {color} {model} at {speed} km/h!")

def render_ce202_simulation():
    """Interactive Simulation for Assembly (CE202)"""
    st.markdown("### ⚙️ Simple Register Simulator (x86)")
    
    # Registers
    if 'eax' not in st.session_state: st.session_state.eax = 0
    if 'ebx' not in st.session_state: st.session_state.ebx = 0
    
    c1, c2 = st.columns(2)
    c1.metric("EAX", f"0x{st.session_state.eax:08X}")
    c2.metric("EBX", f"0x{st.session_state.ebx:08X}")
    
    st.markdown("#### Instructions")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        instr = st.selectbox("Instruction", ["MOV", "ADD", "SUB", "INC", "DEC"])
    with col2:
        target = st.selectbox("Target", ["EAX", "EBX"])
        
    with col3:
        val = 0
        if instr in ["MOV", "ADD", "SUB"]:
            val = st.number_input("Value (Imm)", 0, 100, 5)
            
    if st.button("Execute Step"):
        if instr == "MOV":
            if target == "EAX": st.session_state.eax = val
            else: st.session_state.ebx = val
        elif instr == "ADD":
            if target == "EAX": st.session_state.eax += val
            else: st.session_state.ebx += val
        elif instr == "SUB":
            if target == "EAX": st.session_state.eax -= val
            else: st.session_state.ebx -= val
        elif instr == "INC":
            if target == "EAX": st.session_state.eax += 1
            else: st.session_state.ebx += 1
        elif instr == "DEC":
            if target == "EAX": st.session_state.eax -= 1
            else: st.session_state.ebx -= 1
            
        st.rerun()

def render_ce203_simulation():
    """Interactive Simulation for OS (CE203) - CPU Scheduling"""
    st.markdown("### ⏱️ CPU Scheduling Visualization (FIFO)")
    
    processes = [
        {"id": "P1", "burst": 5, "color": "#ef4444"},
        {"id": "P2", "burst": 3, "color": "#3b82f6"},
        {"id": "P3", "burst": 8, "color": "#10b981"},
        {"id": "P4", "burst": 6, "color": "#f59e0b"}
    ]
    
    # Allow reordering
    st.text("Drag to reorder processes (Simulated by manual input order for now):")
    cols = st.columns(4)
    order = []
    for i, p in enumerate(processes):
        p['order'] = cols[i].number_input(f"{p['id']} Order", 1, 4, i+1)
        
    processes.sort(key=lambda x: x['order'])
    
    # Gantt Chart Calculation
    start_time = 0
    gantt = []
    
    for p in processes:
        gantt.append({
            "Process": p['id'],
            "Start": start_time,
            "End": start_time + p['burst'],
            "Color": p['color']
        })
        start_time += p['burst']
        
    df_gantt = pd.DataFrame(gantt)
    
    chart = alt.Chart(df_gantt).mark_bar().encode(
        x='Start',
        x2='End',
        y='Process',
        color=alt.Color('Process', scale=None, legend=None),
        tooltip=['Process', 'Start', 'End']
    ).properties(height=200)
    
    st.altair_chart(chart, use_container_width=True)
    
    avg_turnaround = sum(x['End'] for x in gantt) / 4
    st.info(f"Average Turnaround Time: {avg_turnaround:.2f} units")

def render_ma201_simulation():
    """Interactive Simulation for Statistics (MA201)"""
    st.markdown("### 📊 Normal Distribution Visualizer")
    
    mu = st.slider("Mean (μ)", -5.0, 5.0, 0.0, 0.5)
    sigma = st.slider("Standard Deviation (σ)", 0.1, 5.0, 1.0, 0.1)
    
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
    y = (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu)/sigma)**2)
    
    df_dist = pd.DataFrame({'x': x, 'Probability Density': y})
    
    area = alt.Chart(df_dist).mark_area(opacity=0.3, color='#3b82f6').encode(
        x='x',
        y='Probability Density'
    )
    line = alt.Chart(df_dist).mark_line(color='#3b82f6').encode(
        x='x',
        y='Probability Density'
    )
    
    st.altair_chart(area + line, use_container_width=True)

def render_ce204_simulation():
    """Interactive Simulation for Algorithms (CE204)"""
    st.markdown("### 🔢 Sorting Algorithm Visualizer")
    
    algo = st.selectbox("Algorithm", ["Bubble Sort", "Quick Sort (Visual Only)"])
    n = st.slider("Number of Elements", 10, 50, 20)
    
    if st.button("Generate New Array"):
        st.session_state.arr = np.random.randint(1, 100, n).tolist()
        
    if 'arr' not in st.session_state:
        st.session_state.arr = np.random.randint(1, 100, n).tolist()
        
    arr = st.session_state.arr.copy()
    
    # Simple Bubble Sort Step-by-Step (Simulated)
    # For a real visualizer we'd need animation, here we show init vs sorted
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Initial Array**")
        st.bar_chart(pd.DataFrame({'Value': arr}))
        
    with col2:
        st.markdown("**Sorted Array**")
        arr.sort()
        st.bar_chart(pd.DataFrame({'Value': arr}))
        
    st.info("ℹ️ Full animation requires more complex state management. This compares Initial vs Sorted states.")
    
    st.code("""
# Bubble Sort Implementation
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    """, language="python")

def render_ce301_simulation():
    """Interactive Simulation for Computer Networks (CE301)"""
    st.markdown("### 🌐 IPv4 Subnet Calculator")
    
    ip_str = st.text_input("IP Address", "192.168.1.1")
    cidr = st.slider("CIDR / Prefix", 1, 32, 24)
    
    try:
        # Simple manual calculation avoiding 'ipaddress' module complexities for now/compatibility
        parts = list(map(int, ip_str.split('.')))
        if len(parts) != 4: raise ValueError
        
        ip_bin = 0
        for p in parts: ip_bin = (ip_bin << 8) + p
        
        mask_bin = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
        net_bin = ip_bin & mask_bin
        broad_bin = net_bin | (~mask_bin & 0xFFFFFFFF)
        
        def to_ip(n):
            return f"{(n >> 24) & 0xFF}.{(n >> 16) & 0xFF}.{(n >> 8) & 0xFF}.{n & 0xFF}"
            
        net_addr = to_ip(net_bin)
        broad_addr = to_ip(broad_bin)
        hosts = (2 ** (32 - cidr)) - 2 if cidr < 31 else 0
        
        col1, col2 = st.columns(2)
        col1.metric("Network Address", net_addr)
        col2.metric("Broadcast Address", broad_addr)
        
        col3, col4 = st.columns(2)
        col3.metric("Subnet Mask", to_ip(mask_bin))
        col4.metric("Usable Hosts", f"{hosts:,}")
        
    except:
        st.error("Invalid IP Address format")

def render_ce304_simulation():
    """Interactive Simulation for Databases (CE304)"""
    st.markdown("### 🗄️ SQL Playground (Mock)")
    
    # Mock Database
    students = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'gpa': [3.8, 3.2, 3.9, 2.5]
    })
    
    st.markdown("**Table: `students`**")
    st.dataframe(students)
    
    query_type = st.radio("Query", ["SELECT *", "SELECT WHERE gpa > 3.5", "COUNT(*)"])
    
    st.markdown("**Result:**")
    if query_type == "SELECT *":
        st.code("SELECT * FROM students;")
        st.dataframe(students)
    elif query_type == "SELECT WHERE gpa > 3.5":
        st.code("SELECT * FROM students WHERE gpa > 3.5;")
        st.dataframe(students[students['gpa'] > 3.5])
    elif query_type == "COUNT(*)":
        st.code("SELECT COUNT(*) FROM students;")
        st.metric("Count", len(students))

def render_bu201_simulation():
    """Interactive Simulation for Processing Industry (BU201)"""
    st.markdown("### 🏭 Production Line Simulator")
    
    st.markdown("Optimize a manufacturing process by balancing speed and quality.")
    
    col1, col2 = st.columns(2)
    with col1:
        batch_size = st.slider("Batch Size", 100, 1000, 500, 50)
        speed = st.slider("Conveyor Speed (m/s)", 1.0, 10.0, 5.0, 0.5)
    
    with col2:
        maintenance = st.slider("Maintenance Freq (%)", 10, 100, 80)
        # Quality drops as speed increases and maintenance decreases
        quality_factor = 1.0 - (speed / 20.0) + (maintenance / 200.0)
        quality = min(max(quality_factor, 0.5), 0.99)
    
    # Simulation Results
    units_produced = int(batch_size * speed * 0.1)
    defects = int(units_produced * (1.0 - quality))
    good_units = units_produced - defects
    revenue = good_units * 5  # $5 per unit
    cost = (units_produced * 2) + (maintenance * 10) # $2 material + maintenance cost
    profit = revenue - cost
    
    st.markdown("#### 📊 Production Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Output", f"{units_produced} units")
    c2.metric("Defects", f"{defects} units", delta=f"-{(1-quality)*100:.1f}%", delta_color="inverse")
    c3.metric("Good Units", f"{good_units} units")
    c4.metric("Net Profit", f"${profit:,.2f}", delta="Profit" if profit > 0 else "Loss")
    
    # Visualization
    df_prod = pd.DataFrame({
        'Category': ['Good Units', 'Defects'],
        'Count': [good_units, defects],
        'Color': ['#10b981', '#ef4444']
    })
    
    chart = alt.Chart(df_prod).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Color", type="nominal", scale=None, legend=None),
        tooltip=['Category', 'Count']
    )
    st.altair_chart(chart, use_container_width=True)

def render_ce303_simulation():
    """Interactive Simulation for Systems Analysis (CE303)"""
    st.markdown("### 📋 Requirements Prioritizer (MoSCoW Method)")
    
    st.markdown("Analyze and prioritize system requirements for an MVP (Minimum Viable Product).")
    
    # Pre-defined requirements for a mock E-commerce App
    if 'reqs' not in st.session_state:
        st.session_state.reqs = [
            {"id": 1, "task": "User Login/Register", "effort": 3, "priority": "Must Have"},
            {"id": 2, "task": "Product Search", "effort": 5, "priority": "Must Have"},
            {"id": 3, "task": "Shopping Cart", "effort": 5, "priority": "Must Have"},
            {"id": 4, "task": "Wishlist", "effort": 2, "priority": "Could Have"},
            {"id": 5, "task": "AI Recommendations", "effort": 8, "priority": "Won't Have"},
            {"id": 6, "task": "Apple Pay Support", "effort": 3, "priority": "Should Have"},
            {"id": 7, "task": "Dark Mode", "effort": 2, "priority": "Could Have"}
        ]
        
    # Interactive Editor
    st.write("#### Backlog Management")
    
    cols = st.columns([3, 1, 2])
    with cols[0]:
        new_task = st.text_input("New Requirement")
    with cols[1]:
        new_effort = st.number_input("Effort (Days)", 1, 10, 3)
    with cols[2]:
        new_prio = st.selectbox("Priority", ["Must Have", "Should Have", "Could Have", "Won't Have"])
        
    if st.button("Add Requirement"):
        if new_task:
            new_id = max([r['id'] for r in st.session_state.reqs]) + 1
            st.session_state.reqs.append({
                "id": new_id, "task": new_task, "effort": new_effort, "priority": new_prio
            })
            
    # Visualizing Priorities
    df_reqs = pd.DataFrame(st.session_state.reqs)
    
    # Calculate Release Metrics
    must_effort = df_reqs[df_reqs['priority'] == 'Must Have']['effort'].sum()
    should_effort = df_reqs[df_reqs['priority'] == 'Should Have']['effort'].sum()
    total_effort = df_reqs['effort'].sum()
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("MVP Effort (Must)", f"{must_effort} days")
    c2.metric("Target Release (Must + Should)", f"{must_effort + should_effort} days")
    c3.metric("Total Scope", f"{total_effort} days")
    
    # Chart
    bar = alt.Chart(df_reqs).mark_bar().encode(
        y=alt.Y('priority', sort=["Must Have", "Should Have", "Could Have", "Won't Have"]),
        x='effort',
        color='priority',
        tooltip=['task', 'effort']
    )
    st.altair_chart(bar, use_container_width=True)

def render_ma301_simulation():
    """Interactive Simulation for Higher Algebra (MA301)"""
    st.markdown("### 🔢 Cyclic Group Visualizer")
    
    st.markdown("Explore the structure of Cyclic Groups $Z_n$ under addition modulo $n$.")
    
    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("Group Order (n)", 3, 20, 12)
    with col2:
        generator = st.slider("Generator (a)", 1, n-1, 1)
        
    # Generate the sequence (subgroup generated by a)
    sequence = [0]
    curr = generator
    while curr != 0:
        sequence.append(curr)
        curr = (curr + generator) % n
        if len(sequence) > n: break # Safety break
        
    # Data for Visualization (Circle Layout)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    # Rotate to start at top (pi/2) and go clockwise (-theta)
    x = np.cos(np.pi/2 - angles)
    y = np.sin(np.pi/2 - angles)
    labels = list(range(n))
    
    nodes = pd.DataFrame({'x': x, 'y': y, 'label': labels})
    
    # Edges for the generated sequence
    edge_data = []
    for i in range(len(sequence)):
        start_idx = sequence[i]
        end_idx = sequence[(i+1)%len(sequence)]
        edge_data.append({
            'x1': x[start_idx], 'y1': y[start_idx],
            'x2': x[end_idx], 'y2': y[end_idx],
            'order': i
        })
    df_edges = pd.DataFrame(edge_data)
    
    # Altair Chart
    base_nodes = alt.Chart(nodes).mark_circle(size=500, color='#6366f1').encode(
        x=alt.X('x', axis=None), y=alt.Y('y', axis=None),
        tooltip=['label']
    )
    
    text_nodes = alt.Chart(nodes).mark_text(dy=0, color='white').encode(
        x='x', y='y', text='label'
    )
    
    edges = alt.Chart(df_edges).mark_line(color='#10b981', strokeWidth=3).encode(
        x='x1', y='y1', x2='x2', y2='y2',
        order='order' # detailed path
    )
    
    st.altair_chart(edges + base_nodes + text_nodes, use_container_width=True)
    
    st.markdown(f"**Subgroup generated by {generator}:** $\\langle {generator} \\rangle = \\{{ {', '.join(map(str, sorted(sequence)))} \\}}$")
    st.info(f"Order of generator $|{generator}|$ is **{len(sequence)}**.")
    if len(sequence) == n:
        st.success(f"Since order equals group size, **{generator}** is a GENERATOR of $Z_{{{n}}}$.")

def render_fi301_simulation():
    """Interactive Simulation for Finance (FI301)"""
    st.markdown("### 💰 Investment Growth Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        principal = st.number_input("Initial Principal ($)", 1000, 1000000, 10000, step=1000)
        rate = st.slider("Annual Interest Rate (%)", 1.0, 15.0, 7.0, 0.1)
    with col2:
        years = st.slider("Time Period (Years)", 5, 40, 20)
        contribution = st.number_input("Monthly Contribution ($)", 0, 5000, 500, step=100)
        
    # Calculate Growth
    data = []
    balance = principal
    monthly_rate = rate / 100 / 12
    
    for month in range(years * 12 + 1):
        if month > 0:
            balance = balance * (1 + monthly_rate) + contribution
        
        if month % 12 == 0: # Record yearly
            year = month // 12
            total_invested = principal + (contribution * month)
            interest = balance - total_invested
            data.append({"Year": year, "Type": "Principal + Contributions", "Amount": total_invested})
            data.append({"Year": year, "Type": "Interest Earned", "Amount": interest})
            
    df_fi = pd.DataFrame(data)
    
    st.markdown(f"#### Future Value: **${balance:,.2f}**")
    
    chart = alt.Chart(df_fi).mark_area().encode(
        x="Year",
        y="Amount",
        color=alt.Color("Type", scale=alt.Scale(domain=['Principal + Contributions', 'Interest Earned'], range=['#94a3b8', '#10b981'])),
        tooltip=["Year", "Type", "Amount"]
    )
    st.altair_chart(chart, use_container_width=True)

def render_it301_simulation():
    """Interactive Simulation for IT (IT301) - Cloud Cost Estimator"""
    st.markdown("### ☁️ Cloud Infrastructure Estimator")
    
    st.caption("Estimate monthly costs for a typical cloud setup (Mock Data).")
    
    inputs = {}
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Compute")
        inputs['vCPUs'] = st.slider("Total vCPUs", 2, 64, 8) * 20 # $20/vcpu
        inputs['RAM (GB)'] = st.slider("Total RAM (GB)", 4, 128, 16) * 5 # $5/gb
        
    with col2:
        st.subheader("Storage & Net")
        inputs['Storage (TB)'] = st.slider("Object Storage (TB)", 1, 50, 5) * 25 # $25/TB
        inputs['Bandwidth (TB)'] = st.slider("Outbound Traffic (TB)", 0, 100, 10) * 80 # $80/TB
        
    total_cost = sum(inputs.values())
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.metric("Estimated Monthly Bill", f"${total_cost:,}")
    
        df_cost = pd.DataFrame([{'Service': k, 'Cost': v} for k, v in inputs.items()])
        
        chart = alt.Chart(df_cost).mark_arc(innerRadius=60).encode(
            theta='Cost',
            color=alt.Color('Service', scale=alt.Scale(scheme='category20b')),
            tooltip=['Service', 'Cost']
        )
        st.altair_chart(chart, use_container_width=True)
        
    with c2:
        st.write("**Breakdown:**")
        st.dataframe(df_cost)

def render_mg301_simulation():
    """Interactive Simulation for Management (MG301) - Gantt Project"""
    st.markdown("### 📅 Project Schedule (Gantt)")
    
    # Mock Project Data
    default_tasks = [
        {"Task": "Market Research", "Start": 0, "Duration": 5, "Phase": "Planning"},
        {"Task": "Prototype Design", "Start": 4, "Duration": 7, "Phase": "Design"},
        {"Task": "Development", "Start": 10, "Duration": 14, "Phase": "Execution"},
        {"Task": "Testing", "Start": 22, "Duration": 5, "Phase": "Execution"},
        {"Task": "Launch", "Start": 26, "Duration": 2, "Phase": "Deployment"}
    ]
    
    df_proj = pd.DataFrame(default_tasks)
    df_proj['End'] = df_proj['Start'] + df_proj['Duration']
    
    # Simple editor (Optional, skipping for brevity to focus on visualization)
    
    chart = alt.Chart(df_proj).mark_bar().encode(
        x='Start',
        x2='End',
        y=alt.Y('Task', sort=None), # Keep original order
        color='Phase',
        tooltip=['Task', 'Start', 'Duration', 'Phase']
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    st.info("Critical Path ends at Day " + str(df_proj['End'].max()))

def render_sd101_simulation():
    """Interactive Simulation for Sustainable Dev (SD101)"""
    st.markdown("### 🌱 Personal Carbon Footprint")
    
    col1, col2 = st.columns(2)
    with col1:
        transport = st.slider("Weekly Driving (km)", 0, 500, 100)
        flights = st.number_input("Flights per Year (Short haul)", 0, 20, 2)
    with col2:
        energy = st.slider("Monthly Electricity (kWh)", 50, 1000, 200)
        meat = st.select_slider("Meat Consumption", options=["None", "Low", "Medium", "High"], value="Medium")
        
    # Mock Calculations (kg CO2 per year)
    co2_transport = transport * 52 * 0.19 
    co2_flights = flights * 500
    co2_energy = energy * 12 * 0.5
    
    meat_factors = {"None": 0, "Low": 500, "Medium": 1500, "High": 3000}
    co2_food = meat_factors[meat]
    
    total = co2_transport + co2_flights + co2_energy + co2_food
    
    st.metric("Annual CO2 Emissions", f"{total/1000:.2f} tonnes")
    
    df_co2 = pd.DataFrame({
        'Source': ['Transport', 'Flights', 'Energy', 'Food'],
        'CO2 (kg)': [co2_transport, co2_flights, co2_energy, co2_food]
    })
    
    chart = alt.Chart(df_co2).mark_bar().encode(
        x='CO2 (kg)',
        y='Source',
        color='Source',
        tooltip=['Source', 'CO2 (kg)']
    )
    if total < 4000: st.success("Great! Your footprint is below average.")
    else: st.warning("Consider reducing flights or energy usage.")

def render_ce401_simulation():
    """Interactive Simulation for Web Development (CE401)"""
    st.markdown("### 🌐 CSS Box Model & Layout Explorer")
    
    st.markdown("Visualize how Margin, Border, and Padding affect an element.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Properties")
        margin = st.slider("Margin (px)", 0, 50, 20)
        padding = st.slider("Padding (px)", 0, 50, 20)
        border = st.slider("Border (px)", 0, 20, 5)
        color = st.color_picker("Content Color", "#3b82f6")
        
        st.subheader("Flexbox")
        justify = st.selectbox("Justify Content", ["flex-start", "center", "flex-end", "space-between"])
        align = st.selectbox("Align Items", ["stretch", "center", "flex-start", "flex-end"])
        
    with col2:
        st.subheader("Live Preview")
        
        # HTML/CSS Construction
        st.markdown(f"""
        <div style="
            display: flex; 
            justify-content: {justify}; 
            align-items: {align};
            background-color: #f1f5f9; 
            border: 2px dashed #94a3b8; 
            height: 300px; 
            padding: 10px;
            border-radius: 8px;">
            <div style="
                margin: {margin}px; 
                padding: {padding}px; 
                border: {border}px solid #1e293b; 
                background-color: {color}; 
                color: white; 
                border-radius: 4px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <strong>Box 1</strong><br>
                M: {margin} | P: {padding}
            </div>
            <div style="
                margin: {margin}px; 
                padding: {padding}px; 
                border: {border}px solid #1e293b; 
                background-color: #ec4899; 
                color: white; 
                border-radius: 4px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <strong>Box 2</strong><br>
                Static
            </div>
        </div>
        <div style="text-align: center; margin-top: 10px; font-family: monospace; color: #64748b;">
            container {{ display: flex; justify-content: {justify}; align-items: {align}; }}
        </div>
        """, unsafe_allow_html=True)

def render_ce402_simulation():
    """Interactive Simulation for AI (CE402) - K-Means Clustering"""
    st.markdown("### 🤖 K-Means Clustering Visualizer")
    
    st.markdown("Unsupervised learning algorithm to group data points.")
    
    col1, col2 = st.columns(2)
    with col1:
        n_points = st.slider("Data Points", 50, 500, 200)
    with col2:
        k = st.slider("Number of Clusters (k)", 2, 6, 3)
        
    if st.button("Generate & Cluster New Data"):
        # Generate random data
        X = np.random.rand(n_points, 2) * 100
        
        # Simple K-Means Implementation
        # 1. Random Centroids
        centroids = X[np.random.choice(X.shape[0], k, replace=False)]
        
        labels = np.zeros(n_points)
        
        # Run a fixed number of iterations (e.g., 10) for demo speed
        for _ in range(10):
            # Assign points to nearest centroid
            distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
            labels = np.argmin(distances, axis=0)
            
            # Update centroids
            new_centroids = np.array([X[labels == i].mean(axis=0) if np.sum(labels==i) > 0 else centroids[i] for i in range(k)])
            
            if np.allclose(centroids, new_centroids):
                break
            centroids = new_centroids
            
        # Store for display
        st.session_state.ai_data = pd.DataFrame({'x': X[:, 0], 'y': X[:, 1], 'cluster': labels.astype(str)})
        st.session_state.ai_centroids = pd.DataFrame({'x': centroids[:, 0], 'y': centroids[:, 1], 'cluster': [f"C{i}" for i in range(k)]})
        
    if 'ai_data' in st.session_state:
        # Scatter Plot
        points = alt.Chart(st.session_state.ai_data).mark_circle(size=60).encode(
            x='x', y='y', color='cluster', tooltip=['x', 'y', 'cluster']
        )
        
        centers = alt.Chart(st.session_state.ai_centroids).mark_point(shape='cross', size=400, color='black', filled=True).encode(
            x='x', y='y', tooltip=['cluster']
        )
        
        st.altair_chart(points + centers, use_container_width=True)
        st.success(f"Converged with k={k} clusters.")
    else:
        st.info("Click the button to run the AI algorithm.")



def render_ce403_simulation():
    """Interactive Simulation for Mobile App Dev (CE403)"""
    st.markdown("### 📱 Mobile UI Density Calculator")
    st.markdown("Understand the relationship between Resolution (px), Density (dpi), and Abstract Units (dp/pt).")
    
    col1, col2 = st.columns(2)
    with col1:
        width_px = st.number_input("Screen Width (px)", 320, 4000, 1080)
        height_px = st.number_input("Screen Height (px)", 480, 8000, 1920)
        diag_inch = st.number_input("Diagonal Size (inch)", 3.0, 12.0, 6.0, step=0.1)
        
    # Calcs
    ppi = np.sqrt(width_px**2 + height_px**2) / diag_inch
    
    # Classification
    bucket = "mdpi (1x)"
    scale = 1.0
    if ppi > 160: bucket, scale = "hdpi (1.5x)", 1.5
    if ppi > 240: bucket, scale = "xhdpi (2.0x)", 2.0
    if ppi > 320: bucket, scale = "xxhdpi (3.0x)", 3.0
    if ppi > 480: bucket, scale = "xxxhdpi (4.0x)", 4.0
    
    width_dp = width_px / scale
    height_dp = height_px / scale
    
    with col2:
        st.info(f"Pixel Density: **{ppi:.2f} ppi**")
        st.success(f"Density Bucket: **{bucket}**")
        st.metric("Width (dp)", f"{width_dp:.0f} dp")
        st.metric("Height (dp)", f"{height_dp:.0f} dp")
        
    st.caption(f"Designing at 1x (mdpi), your canvas should be {width_dp:.0f} x {height_dp:.0f}.")

def render_ce404_simulation():
    """Interactive Simulation for Cloud Computing (CE404)"""
    st.markdown("### ⚖️ Load Balancer Simulator")
    st.markdown("Distribute incoming web traffic across multiple server instances.")
    
    traffic = st.slider("Incoming Requests per Second", 100, 5000, 1000)
    servers = st.slider("Number of Active Servers", 1, 10, 2)
    algorithm = st.selectbox("Balancing Algorithm", ["Round Robin", "Least Connections (Mock)", "IP Hash (Mock)"])
    
    if servers > 0:
        load_per_server = traffic / servers
        st.write(f"Estimated Load: **{load_per_server:.0f} req/sec** per server")
        
        # Visualize Server Load
        load_data = []
        for i in range(servers):
            # Add some randomness for realism
            variance = np.random.randint(-50, 50)
            actual_load = max(0, load_per_server + variance)
            status = "Healthy" if actual_load < 800 else "Overloaded"
            load_data.append({"Server": f"Server {i+1}", "Load": actual_load, "Status": status})
            
        df_cloud = pd.DataFrame(load_data)
        
        chart = alt.Chart(df_cloud).mark_bar().encode(
            x='Server',
            y='Load',
            color=alt.Color('Status', scale=alt.Scale(domain=['Healthy', 'Overloaded'], range=['#34d399', '#f87171'])),
            tooltip=['Server', 'Load', 'Status']
        )
        st.altair_chart(chart, use_container_width=True)
        
        if load_per_server > 800:
            st.error("⚠️ Servers are under heavy load! Scale up (add instances).")
        else:
            st.success("✅ System is stable.")

def render_ce405_simulation():
    """Interactive Simulation for Cybersecurity (CE405)"""
    import hashlib
    st.markdown("### 🔐 Hash Cracker & Entropy Checker")
    
    password = st.text_input("Test a Password (not your real one!)", type="password")
    
    if password:
        # 1. Entropy / Strength
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        score = length * 4
        if has_upper: score += 5
        if has_lower: score += 5
        if has_digit: score += 10
        if has_special: score += 15
        
        st.write("Strength Score:", score)
        st.progress(min(score, 100))
        
        # 2. Hashing
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        sha256_hash = hashlib.sha256(password.encode()).hexdigest()
        
        st.code(f"MD5:    {md5_hash}", language="text")
        st.code(f"SHA256: {sha256_hash}", language="text")
        
        st.caption("Notice: Even a small change in password completely changes the hash (Avalanche Effect).")

def render_ce406_simulation():
    """Interactive Simulation for Big Data (CE406)"""
    st.markdown("### 🐘 MapReduce Visualizer (Word Count)")
    
    text_input = st.text_area("Input Text Corpus", "Big data is big. Data is data. Big insights from big data.")
    
    if text_input:
        st.write("#### 1. Map Phase (Splitting & Mapping)")
        clean_text = ''.join(c.lower() if c.isalnum() or c.isspace() else ' ' for c in text_input)
        words = clean_text.split()
        mapped = [(w, 1) for w in words]
        st.write(mapped[:10], "... (sampled)")
        
        st.write("#### 2. Shuffle & Sort")
        grouped = {}
        for k, v in mapped:
            if k not in grouped: grouped[k] = []
            grouped[k].append(v)
        st.write(grouped)
        
        st.write("#### 3. Reduce Phase (Aggregation)")
        reduced = {k: sum(v) for k, v in grouped.items()}
        st.write(reduced)
        
        # Visualize
        df_reduce = pd.DataFrame(list(reduced.items()), columns=['Word', 'Count']).sort_values('Count', ascending=False)
        chart = alt.Chart(df_reduce).mark_bar().encode(
            x=alt.X('Count'),
            y=alt.Y('Word', sort='-x'),
            tooltip=['Word', 'Count']
        )
        st.altair_chart(chart, use_container_width=True)

def render_ce407_simulation():
    """Interactive Simulation for Blockchain (CE407)"""
    import hashlib
    st.markdown("### ⛓️ Blockchain Mining Demo")
    
    block_number = st.number_input("Block Number", 1, 1000, 1)
    data = st.text_input("Block Data", "Alice pays Bob 5 BTC")
    difficulty = st.slider("Difficulty (Leading Zeros)", 1, 5, 3)
    
    st.write("Mining...")
    nonce = 0
    target_prefix = "0" * difficulty
    
    # Mining Loop (Limited for browser perf)
    found = False
    max_iter = 100000
    
    status_text = st.empty()
    
    if st.button("Start Mining"):
        with st.spinner(f"Mining (Searching for hash starting with '{target_prefix}')..."):
            for i in range(max_iter):
                text = f"{block_number}{data}{nonce}"
                hash_result = hashlib.sha256(text.encode()).hexdigest()
                
                if hash_result.startswith(target_prefix):
                    found = True
                    break
                nonce += 1
                
        if found:
            st.success(f"Block Mined! Nonce: {nonce}")
            st.write(f"**Hash:** `{hash_result}`")
        else:
            st.error(f"Gave up after {max_iter} iterations. Try easier difficulty or simpler data.")

def render_ce408_simulation():
    """Interactive Simulation for IoT (CE408)"""
    st.markdown("### 🏠 Smart Home IoT Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Living Room Temp", "24.5 °C", "0.5 °C")
    col2.metric("Humidity", "55 %", "-2 %")
    col3.metric("Lights", "ON", delta_color="off")
    
    # Real-time Stream Simulation
    st.subheader("Sensor Data Stream")
    
    if 'iot_data' not in st.session_state:
        st.session_state.iot_data = pd.DataFrame(columns=['Time', 'Value', 'Sensor'])
        
    # Simulate new data point (mock)
    new_time = len(st.session_state.iot_data)
    new_temp = 24 + np.random.normal(0, 0.5)
    new_hum = 55 + np.random.normal(0, 2.0)
    
    # Append (in a real app this would use a loop/callback, here we just show chart logic)
    # Let's generate a static history chart instead of auto-updating loop to avoid streamlit blocking
    
    time_points = list(range(24)) # 24 hours
    temps = [24 + np.random.normal(0, 1) + np.sin(t/4)*2 for t in time_points]
    hums = [50 + np.random.normal(0, 2) - np.sin(t/4)*5 for t in time_points]
    
    df_iot = pd.DataFrame({
        'Hour': time_points * 2,
        'Value': temps + hums,
        'Sensor': ['Temperature'] * 24 + ['Humidity'] * 24
    })
    
    chart = alt.Chart(df_iot).mark_line(point=True).encode(
        x='Hour',
        y='Value',
        color='Sensor',
        tooltip=['Hour', 'Value', 'Sensor']
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

# Map course ID to simulation function
SIMULATION_MAP = {
    "MA101": render_ma101_simulation,
    "MA102": render_ma102_simulation,
    "CE101": render_ce101_simulation,
    "PH101": render_ph101_simulation,
    "CE302": render_ce302_simulation,
    "CE103": render_ce103_simulation,
    "EE101": render_ee101_simulation,
    "CE201": render_ce201_simulation,
    "CE202": render_ce202_simulation,
    "CE203": render_ce203_simulation,
    "MA201": render_ma201_simulation,
    "CE204": render_ce204_simulation,
    "CE301": render_ce301_simulation,
    "CE304": render_ce304_simulation,
    "BU201": render_bu201_simulation,
    "CE303": render_ce303_simulation,
    "MA301": render_ma301_simulation,
    "FI301": render_fi301_simulation,
    "IT301": render_it301_simulation,
    "MG301": render_mg301_simulation,
    "SD101": render_sd101_simulation,
    "CE401": render_ce401_simulation,
    "CE402": render_ce402_simulation,
    "CE403": render_ce403_simulation,
    "CE404": render_ce404_simulation,
    "CE405": render_ce405_simulation,
    "CE406": render_ce406_simulation,
    "CE407": render_ce407_simulation,
    "CE408": render_ce408_simulation
}
