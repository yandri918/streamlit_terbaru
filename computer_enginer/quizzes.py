import streamlit as st
import time

def render_quiz(course_data):
    """Renders a mock exam/quiz for the given course."""
    
    st.markdown(f"### 📝 {course_data['name']} - Final Exam")
    st.caption("Pass this exam to earn your certificate.")
    
    # Initialize Quiz State
    quiz_key = f"quiz_{course_data['id']}_started"
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = False
        
    if not st.session_state[quiz_key]:
        st.info("Time Limit: 30 Minutes • Questions: 5 • Passing Score: 80%")
        if st.button("Start Exam", key=f"start_{course_data['id']}", type="primary"):
            st.session_state[quiz_key] = True
            st.rerun()
    else:
        # REALISTIC QUESTION BANK (International Curriculum Standard)
        QUESTION_BANK = {
            # --- SEMESTER 1 ---
            "MA101": [ # Calculus
                {"q": "Evaluate: lim(x->0) (sin x / x)", "options": ["0", "1", "Infinity", "Undefined"], "correct": "1"},
                {"q": "What is the derivative of f(x) = e^x?", "options": ["x*e^(x-1)", "e^x", "ln(x)", "e"], "correct": "e^x"},
                {"q": "The integral of 1/x dx is:", "options": ["ln|x| + C", "-1/x^2", "e^x + C", "x^2/2"], "correct": "ln|x| + C"},
                {"q": "If f'(x) > 0 on an interval, then f(x) is:", "options": ["Decreasing", "Constant", "Increasing", "Concave Up"], "correct": "Increasing"},
                {"q": "Find the critical points of f(x) = x^3 - 3x", "options": ["x=0, x=1", "x=1, x=-1", "x=0", "x=3"], "correct": "x=1, x=-1"}
            ],
            "CE101": [ # Programming (Python/C)
                {"q": "What is the time complexity of binary search?", "options": ["O(n)", "O(n^2)", "O(log n)", "O(1)"], "correct": "O(log n)"},
                {"q": "Which data structure uses LIFO (Last In First Out)?", "options": ["Queue", "Stack", "Array", "Linked List"], "correct": "Stack"},
                {"q": "In Python, which keyword is used to define a function?", "options": ["func", "define", "def", "function"], "correct": "def"},
                {"q": "What is the result of 3 // 2 in Python?", "options": ["1.5", "1", "2", "Syntax Error"], "correct": "1"},
                {"q": "Which pattern is best for a one-to-many dependency?", "options": ["Singleton", "Observer", "Factory", "Decorator"], "correct": "Observer"}
            ],
            
            # --- SEMESTER 4 ---
            "CE204": [ # Algorithms
                {"q": "Which sorting algorithm has the best average case time complexity?", "options": ["Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort"], "correct": "Merge Sort"},
                {"q": "Dijkstra's algorithm is used for:", "options": ["Sorting", "Shortest Path in Graph", "Minimal Spanning Tree", "String Matching"], "correct": "Shortest Path in Graph"},
                {"q": "What is the worst-case complexity of QuickSort?", "options": ["O(n log n)", "O(n)", "O(n^2)", "O(log n)"], "correct": "O(n^2)"},
                {"q": "Dynamic Programming is best described as:", "options": ["Recursive brute force", "Breaking problems into overlapping subproblems", "Greedy choice property", "Randomized approach"], "correct": "Breaking problems into overlapping subproblems"},
                {"q": "Which of these is NOT a P-NP problem class?", "options": ["P", "NP", "NP-Complete", "Big-O"], "correct": "Big-O"}
            ],
             "CE302": [ # Digital Systems
                {"q": "Which logic gate outputs 1 only if both inputs are 1?", "options": ["OR", "XOR", "AND", "NAND"], "correct": "AND"},
                {"q": "A collection of 8 bits is called a:", "options": ["Nibble", "Word", "Byte", "Bit"], "correct": "Byte"},
                {"q": "What does a Flip-Flop store?", "options": ["1 Bit of Data", "1 Byte of Data", "Analog Signal", "Voltage"], "correct": "1 Bit of Data"},
                {"q": "In Boulean Algebra, A + A' equals:", "options": ["0", "1", "A", "A'"], "correct": "1"},
                {"q": "Which circuit is known as a Data Selector?", "options": ["Encoder", "Decoder", "Multiplexer", "Demultiplexer"], "correct": "Multiplexer"}
            ],

            # --- SEMESTER 7 ---
            "CE402": [ # AI
                {"q": "Which algorithm is commonly used for classification problems?", "options": ["K-Means", "Linear Regression", "Support Vector Machine (SVM)", "Apriori"], "correct": "Support Vector Machine (SVM)"},
                {"q": "What is 'Overfitting' in Machine Learning?", "options": ["Model performs well on training data but poor on test data", "Model performs poor on both", "Model is too simple", "Dataset is too small"], "correct": "Model performs well on training data but poor on test data"},
                {"q": "Which activation function is used for binary classification?", "options": ["ReLU", "Softmax", "Sigmoid", "Tanh"], "correct": "Sigmoid"},
                {"q": "What does CNN stand for in Deep Learning?", "options": ["Central Neural Network", "Convolutional Neural Network", "Computer Neural Network", "Cyber Neural Network"], "correct": "Convolutional Neural Network"},
                {"q": "Reinforcement Learning is based on:", "options": ["Supervised Labels", "Unsupervised Clustering", "Agents, Actions, and Rewards", "Regression Analysis"], "correct": "Agents, Actions, and Rewards"}
            ],

            # --- SEMESTER 8 ---
            "CE407": [ # Blockchain
                {"q": "What is the primary mechanism Bitcoin uses for consensus?", "options": ["Proof of Stake", "Proof of Work", "Proof of History", "Delegated PoS"], "correct": "Proof of Work"},
                {"q": "What is a 'Smart Contract'?", "options": ["A legal paper document", "Self-executing code on the blockchain", "A contract signed by AI", "A secure email"], "correct": "Self-executing code on the blockchain"},
                {"q": "Which attack involves a miner controlling >50% of the network?", "options": ["Sybil Attack", "51% Attack", "DDoS", "Phishing"], "correct": "51% Attack"},
                {"q": "What is 'Gas' in Ethereum?", "options": ["Fuel for servers", "Fee for computation", "A token for voting", "Nothing"], "correct": "Fee for computation"},
                {"q": "Which property ensures that once data is written, it cannot be changed?", "options": ["Transparent", "Immutability", "Decentralization", "Anonymity"], "correct": "Immutability"}
            ],
            "CE405": [ # Cybersecurity
                {"q": "What does 'Phishing' refer to?", "options": ["Network scanning", "Fraudulent emails to steal credentials", "Brute force attack", "Encrypting data"], "correct": "Fraudulent emails to steal credentials"},
                {"q": "Which principle is NOT part of the CIA Triad?", "options": ["Confidentiality", "Integrity", "Availability", "Authorization"], "correct": "Authorization"},
                {"q": "What is a 'Zero Day' vulnerability?", "options": ["A bug known for 0 days (unknown to vendor)", "A virus that lasts 0 days", "A patch released on Sunday", "A weak password"], "correct": "A bug known for 0 days (unknown to vendor)"},
                {"q": "Symmetric encryption uses:", "options": ["Two different keys", "The same key for encryption and decryption", "No keys", "Public and Private keys"], "correct": "The same key for encryption and decryption"},
                {"q": "What is a Denial of Service (DoS) attack?", "options": ["Stealing data", "Overwhelming a system to make it unavailable", "Guessing passwords", "Injecting SQL"], "correct": "Overwhelming a system to make it unavailable"}
            ],
            "CE408": [ # IoT
                {"q": "Which protocol is lightweight and often used in IoT?", "options": ["HTTP", "MQTT", "FTP", "SMTP"], "correct": "MQTT"},
                {"q": "What is the role of an 'Actuator'?", "options": ["Sense the environment", "Perform a physical action", "Process data", "Store energy"], "correct": "Perform a physical action"},
                {"q": "IoT devices often operate on what kind of network?", "options": ["High Latency", "Low Power Wide Area Network (LPWAN)", "Wired LAN only", "Mainframe"], "correct": "Low Power Wide Area Network (LPWAN)"},
                {"q": "Which is a major security concern in IoT?", "options": ["Devices are too expensive", "Weak default passwords", "Too much processing power", "High energy consumption"], "correct": "Weak default passwords"},
                {"q": "Edge Computing processes data:", "options": ["In a centralized cloud", "Closer to the source (device)", "On paper", "In a far remote server"], "correct": "Closer to the source (device)"}
            ]
        }
        
        # Select questions based on Course ID, or fallback to generic
        questions = QUESTION_BANK.get(course_data['id'])
        
        if not questions:
             # Generic Fallback for courses not yet fully populated
             questions = [
                {"q": f"What is a core learning outcome of {course_data['name']}?", "options": ["Understanding fundamental principles", "Memorizing facts", "Ignoring theory", "None of the above"], "correct": "Understanding fundamental principles"},
                {"q": "This course primarily deals with:", "options": ["Computer Engineering concepts", " Culinary Arts", "Marine Biology", "Astrophysics"], "correct": "Computer Engineering concepts"},
                {"q": "Which skill is most relevant to this subject?", "options": ["Problem Solving", "Singing", "Gardening", "Painting"], "correct": "Problem Solving"},
                {"q": "In a professional setting, this knowledge is used for:", "options": ["Designing and optimizing systems", "Entertainment only", "Manual labor", "Guesswork"], "correct": "Designing and optimizing systems"},
                {"q": "Why is this subject important?", "options": ["It builds the foundation for advanced topics", "It is optional", "It is outdated", "It is easy"], "correct": "It builds the foundation for advanced topics"}
            ]
        
        # Render Form
        with st.form(key=f"exam_form_{course_data['id']}"):
            score = 0
            user_answers = {}
            
            for i, q in enumerate(questions):
                st.markdown(f"**{i+1}. {q['q']}**")
                user_answers[i] = st.radio(f"Select answer for Q{i+1}", q['options'], key=f"q_{course_data['id']}_{i}", label_visibility="collapsed")
                st.divider()
                
            submitted = st.form_submit_button("Submit Exam")
            
            if submitted:
                # Calculate Score
                correct_count = 0
                for i, q in enumerate(questions):
                    if user_answers[i] == q['correct']:
                        correct_count += 1
                
                final_score = (correct_count / len(questions)) * 100
                
                if final_score >= 80:
                    st.balloons()
                    st.success(f"🎉 Congratulations! You Passed! Score: {final_score:.0f}%")
                    
                    # Generate Certificate Logic
                    try:
                        from pdf_utils import generate_certificate_pdf
                        pdf_bytes = generate_certificate_pdf("Student User", course_data['name'], final_score)
                        
                        col_c1, col_c2 = st.columns([1, 2])
                        with col_c1:
                            st.download_button(
                                label="📜 Download Certified PDF",
                                data=pdf_bytes,
                                file_name=f"Certificate_{course_data['id']}.pdf",
                                mime="application/pdf",
                                type="primary"
                            )
                        with col_c2:
                            st.info("Your official digital certificate is ready for download.")
                            
                    except ImportError:
                         # Fallback if pdf_utils missing
                        st.markdown("""
                        <div style="padding: 20px; background-color: #f0fdf4; border: 2px solid #16a34a; border-radius: 10px; text-align: center; margin-top: 20px;">
                            <h2 style="color: #166534; margin:0;">CERTIFICATE OF COMPLETION</h2>
                            <p style="color: #15803d;">This certifies that</p>
                            <h3 style="color: #1e293b;">Student User</h3>
                            <p>has successfully completed the course</p>
                            <h3 style="color: #1e293b;">""" + course_data['name'] + """</h3>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error(f"Score: {final_score:.0f}%. You did not pass. Please try again.")
