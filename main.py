import sqlite3
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, JobQueue
)
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

DB_PATH = "gateprep.db"

# --- DB FUNCTIONS ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id TEXT PRIMARY KEY,
            name TEXT,
            reminder_time TEXT DEFAULT '07:00',
            current_day INTEGER DEFAULT 1
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            day INTEGER PRIMARY KEY,
            topic TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            telegram_id TEXT,
            day INTEGER,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    # Add sample 7-day schedule
    cur.executemany('INSERT OR IGNORE INTO schedule (day, topic) VALUES (?, ?)', [
        (1, 'Digital Logic: Number Systems'),
        (2, 'Digital Logic: Boolean Algebra'),
        (3, 'Digital Logic: K-Maps'),
        (4, 'Digital Logic: Combinational Circuits'),
        (5, 'Digital Logic: Sequential Circuits'),
        (6, 'Digital Logic: Minimization'),
        (7, 'Computer Networks: OSI Model'),
        (8, 'Computer Networks: TCP/IP Stack'),
        (9, 'Computer Networks: Routing Protocols'),
        (10, 'Computer Networks: IP Addressing'),
        (11, 'Computer Networks: Transport Layer'),
        (12, 'Computer Networks: Application Layer Protocols'),
        (13, 'Operating Systems: Process Scheduling'),
        (14, 'Operating Systems: Process Synchronization'),
        (15, 'Operating Systems: Memory Management'),
        (16, 'Operating Systems: Virtual Memory'),
        (17, 'Operating Systems: File Systems'),
        (18, 'Algorithms: Sorting Algorithms'),
        (19, 'Algorithms: Searching Algorithms'),
        (20, 'Algorithms: Recursion and Backtracking'),
        (21, 'Algorithms: Greedy Algorithms'),
        (22, 'Algorithms: Dynamic Programming'),
        (23, 'Algorithms: Graph Algorithms'),
        (24, 'Programming & DS: Arrays and Strings'),
        (25, 'Programming & DS: Stacks and Queues'),
        (26, 'Programming & DS: Linked Lists'),
        (27, 'Programming & DS: Trees'),
        (28, 'Programming & DS: Graphs'),
        (29, 'Computer Organization: Instruction Set'),
        (30, 'Computer Organization: ALU and Data Path'),
        (31, 'Computer Organization: Pipelining'),
        (32, 'Computer Organization: Cache and Memory'),
        (33, 'Computer Organization: I/O and DMA'),
        (34, 'DBMS: ER Models'),
        (35, 'DBMS: Relational Algebra'),
        (36, 'DBMS: SQL Queries'),
        (37, 'DBMS: Normalization'),
        (38, 'DBMS: Indexing and Transactions'),
        (39, 'TOC: Regular Expressions and FA'),
        (40, 'TOC: CFG and PDA'),
        (41, 'TOC: Pumping Lemma'),
        (42, 'TOC: Turing Machines and Decidability'),
        (43, 'Compiler Design: Lexical Analysis'),
        (44, 'Compiler Design: Parsing'),
        (45, 'Compiler Design: Intermediate Code Generation'),
        (46, 'Compiler Design: Code Optimization'),
        (47, 'Maths: Set Theory and Logic'),
        (48, 'Maths: Graph Theory'),
        (49, 'Maths: Linear Algebra'),
        (50, 'Maths: Calculus'),
        (51, 'Maths: Probability and Statistics'),
        (52, 'Digital Logic: Number Systems'),
        (53, 'Digital Logic: Boolean Algebra'),
        (54, 'Digital Logic: K-Maps'),
        (55, 'Digital Logic: Combinational Circuits'),
        (56, 'Digital Logic: Sequential Circuits'),
        (57, 'Digital Logic: Minimization'),
        (58, 'Computer Networks: OSI Model'),
        (59, 'Computer Networks: TCP/IP Stack'),
        (60, 'Computer Networks: Routing Protocols'),
        (61, 'Computer Networks: IP Addressing'),
        (62, 'Computer Networks: Transport Layer'),
        (63, 'Computer Networks: Application Layer Protocols'),
        (64, 'Operating Systems: Process Scheduling'),
        (65, 'Operating Systems: Process Synchronization'),
        (66, 'Operating Systems: Memory Management'),
        (67, 'Operating Systems: Virtual Memory'),
        (68, 'Operating Systems: File Systems'),
        (69, 'Algorithms: Sorting Algorithms'),
        (70, 'Algorithms: Searching Algorithms'),
        (71, 'Algorithms: Recursion and Backtracking'),
        (72, 'Algorithms: Greedy Algorithms'),
        (73, 'Algorithms: Dynamic Programming'),
        (74, 'Algorithms: Graph Algorithms'),
        (75, 'Programming & DS: Arrays and Strings'),
        (76, 'Programming & DS: Stacks and Queues'),
        (77, 'Programming & DS: Linked Lists'),
        (78, 'Programming & DS: Trees'),
        (79, 'Programming & DS: Graphs'),
        (80, 'Computer Organization: Instruction Set'),
        (81, 'Computer Organization: ALU and Data Path'),
        (82, 'Computer Organization: Pipelining'),
        (83, 'Computer Organization: Cache and Memory'),
        (84, 'Computer Organization: I/O and DMA'),
        (85, 'DBMS: ER Models'),
        (86, 'DBMS: Relational Algebra'),
        (87, 'DBMS: SQL Queries'),
        (88, 'DBMS: Normalization'),
        (89, 'DBMS: Indexing and Transactions'),
        (90, 'TOC: Regular Expressions and FA'),
        (91, 'TOC: CFG and PDA'),
        (92, 'TOC: Pumping Lemma'),
        (93, 'TOC: Turing Machines and Decidability'),
        (94, 'Compiler Design: Lexical Analysis'),
        (95, 'Compiler Design: Parsing'),
        (96, 'Compiler Design: Intermediate Code Generation'),
        (97, 'Compiler Design: Code Optimization'),
        (98, 'Maths: Set Theory and Logic'),
        (99, 'Maths: Graph Theory'),
        (100, 'Maths: Linear Algebra'),
        (101, 'Maths: Calculus'),
        (102, 'Maths: Probability and Statistics'),
        (103, 'Digital Logic: Number Systems'),
        (104, 'Digital Logic: Boolean Algebra'),
        (105, 'Digital Logic: K-Maps'),
        (106, 'Digital Logic: Combinational Circuits'),
        (107, 'Digital Logic: Sequential Circuits'),
        (108, 'Digital Logic: Minimization'),
        (109, 'Computer Networks: OSI Model'),
        (110, 'Computer Networks: TCP/IP Stack'),
        (111, 'Computer Networks: Routing Protocols'),
        (112, 'Computer Networks: IP Addressing'),
        (113, 'Computer Networks: Transport Layer'),
        (114, 'Computer Networks: Application Layer Protocols'),
        (115, 'Operating Systems: Process Scheduling'),
        (116, 'Operating Systems: Process Synchronization'),
        (117, 'Operating Systems: Memory Management'),
        (118, 'Operating Systems: Virtual Memory'),
        (119, 'Operating Systems: File Systems'),
        (120, 'Algorithms: Sorting Algorithms'),
        (121, 'Algorithms: Searching Algorithms'),
        (122, 'Algorithms: Recursion and Backtracking'),
        (123, 'Algorithms: Greedy Algorithms'),
        (124, 'Algorithms: Dynamic Programming'),
        (125, 'Algorithms: Graph Algorithms'),
        (126, 'Programming & DS: Arrays and Strings'),
        (127, 'Programming & DS: Stacks and Queues'),
        (128, 'Programming & DS: Linked Lists'),
        (129, 'Programming & DS: Trees'),
        (130, 'Programming & DS: Graphs'),
        (131, 'Computer Organization: Instruction Set'),
        (132, 'Computer Organization: ALU and Data Path'),
        (133, 'Computer Organization: Pipelining'),
        (134, 'Computer Organization: Cache and Memory'),
        (135, 'Computer Organization: I/O and DMA'),
        (136, 'DBMS: ER Models'),
        (137, 'DBMS: Relational Algebra'),
        (138, 'DBMS: SQL Queries'),
        (139, 'DBMS: Normalization'),
        (140, 'DBMS: Indexing and Transactions'),
        (141, 'TOC: Regular Expressions and FA'),
        (142, 'TOC: CFG and PDA'),
        (143, 'TOC: Pumping Lemma'),
        (144, 'TOC: Turing Machines and Decidability'),
        (145, 'Compiler Design: Lexical Analysis'),
        (146, 'Compiler Design: Parsing'),
        (147, 'Compiler Design: Intermediate Code Generation'),
        (148, 'Compiler Design: Code Optimization'),
        (149, 'Maths: Set Theory and Logic'),
        (150, 'Maths: Graph Theory'),
        (151, 'Maths: Linear Algebra'),
        (152, 'Maths: Calculus'),
        (153, 'Maths: Probability and Statistics'),
        (154, 'Digital Logic: Number Systems'),
        (155, 'Digital Logic: Boolean Algebra'),
        (156, 'Digital Logic: K-Maps'),
        (157, 'Digital Logic: Combinational Circuits'),
        (158, 'Digital Logic: Sequential Circuits'),
        (159, 'Digital Logic: Minimization'),
        (160, 'Computer Networks: OSI Model'),
        (161, 'Computer Networks: TCP/IP Stack'),
        (162, 'Computer Networks: Routing Protocols'),
        (163, 'Computer Networks: IP Addressing'),
        (164, 'Computer Networks: Transport Layer'),
        (165, 'Computer Networks: Application Layer Protocols'),
        (166, 'Operating Systems: Process Scheduling'),
        (167, 'Operating Systems: Process Synchronization'),
        (168, 'Operating Systems: Memory Management'),
        (169, 'Operating Systems: Virtual Memory'),
        (170, 'Operating Systems: File Systems'),
        (171, 'Algorithms: Sorting Algorithms'),
        (172, 'Algorithms: Searching Algorithms'),
        (173, 'Algorithms: Recursion and Backtracking'),
        (174, 'Algorithms: Greedy Algorithms'),
        (175, 'Algorithms: Dynamic Programming'),
        (176, 'Algorithms: Graph Algorithms'),
        (177, 'Programming & DS: Arrays and Strings'),
        (178, 'Programming & DS: Stacks and Queues'),
        (179, 'Programming & DS: Linked Lists'),
        (180, 'Programming & DS: Trees')
    ])
    conn.commit()
    conn.close()

def get_topic(day):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT topic FROM schedule WHERE day = ?", (day,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_user(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cur.fetchone()
    conn.close()
    return user

def add_user(telegram_id, name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
    conn.commit()
    conn.close()

def increment_day(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET current_day = current_day + 1 WHERE telegram_id = ?", (telegram_id,))
    conn.commit()
    conn.close()

# --- COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name
    add_user(user_id, name)
    await update.message.reply_text(
        f"👋 Hi {name}, welcome to GATE Prep Bot!"
        "You'll receive a daily concept reminder. Use /startprep to begin."
    )

async def start_prep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user = get_user(user_id)
    if not user:
        await update.message.reply_text("Please use /start first.")
        return
    # Send today's concept immediately
    day = user[3]
    topic = get_topic(day)
    if topic:
        keyboard = [
            [InlineKeyboardButton("✅ Mark as Done", callback_data="done")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"📚 GATE Concept for\nDay {day}\n*{topic}*",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("🎉 You've completed all scheduled topics!")
        return
    # Schedule future reminders
    schedule_reminder(context.application.job_queue, user_id, user[2])
    await update.message.reply_text("✅ Daily reminders scheduled! You will receive the next concept tomorrow.")

# --- DAILY JOB ---
async def send_daily_concept(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    telegram_id = job_data["telegram_id"]
    user = get_user(telegram_id)
    if not user:
        return
    day = user[3]
    topic = get_topic(day)
    if not topic:
        await context.bot.send_message(chat_id=telegram_id, text="🎉 You've completed all scheduled topics!")
        return
    keyboard = [
        [InlineKeyboardButton("✅ Mark as Done", callback_data="done")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=telegram_id, text=f"📚 GATE Concept for Day {day}:*{topic}*", parse_mode="Markdown", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    telegram_id = str(query.from_user.id)
    if query.data == "done":
        increment_day(telegram_id)
        user = get_user(telegram_id)
        day = user[3]
        topic = get_topic(day)
        if topic:
            # Prepend "Marked as done" above the old message
            old_text = query.message.text
            new_text = f"✅ Marked as done.\n\n{old_text}"
            keyboard = [
                [InlineKeyboardButton("➡️ Next Concept", callback_data="next")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                new_text,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            reschedule_reminder(context, telegram_id, user[2])
        else:
            await query.edit_message_text("🎉 You've completed all scheduled topics!")
    elif query.data == "next":
        user = get_user(telegram_id)
        day = user[3]
        topic = get_topic(day)
        if topic:
            keyboard = [
                [InlineKeyboardButton("✅ Mark as Done", callback_data="done")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=telegram_id,
                text=f"📚 GATE Concept for\nDay {day}\n*{topic}*",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(
                chat_id=telegram_id,
                text="🎉 You've completed all scheduled topics!"
            )

# --- JOB SCHEDULING ---
def schedule_reminder(job_queue: JobQueue, telegram_id: str, time_str: str):
    hour, minute = map(int, time_str.split(":"))
    job_queue.run_daily(
        send_daily_concept,
        time=datetime.time(hour=hour, minute=minute),
        data={"telegram_id": telegram_id},
        name=f"reminder_{telegram_id}",
        chat_id=telegram_id
    )

def reschedule_reminder(context, telegram_id, time_str):
    # Remove old job if exists
    job_queue = context.application.job_queue
    job_name = f"reminder_{telegram_id}"
    old_jobs = job_queue.get_jobs_by_name(job_name)
    for job in old_jobs:
        job.schedule_removal()
    # Schedule new job for the next day
    schedule_reminder(job_queue, telegram_id, time_str)

# --- MAIN APP ---
if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("startprep", start_prep))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()