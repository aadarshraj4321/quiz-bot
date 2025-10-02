from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id and current_question_id != 0:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        bot_responses.append(error)
        question_text, _ = get_next_question(current_question_id - 1 if current_question_id is not None else None)
        if question_text:
            bot_responses.append(question_text)
        return bot_responses

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the answer for the current question to django session.
    """
    if current_question_id is None:
        return True, ""

    # so i have to initialize user_answers in session if it doesnt exist
    if 'user_answers' not in session:
        session['user_answers'] = []

    question = PYTHON_QUESTION_LIST[current_question_id]
    
    if answer.lower() not in question['options']:
        error_message = f"Invalid option '{answer}'. Please choose from the available options."
        return False, error_message

    # we have to store the user answer
    session['user_answers'].append({
        "question_id": current_question_id,
        "user_answer": answer.lower()
    })
    
    return True, ""


def get_next_question(current_question_id):
    """
    fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    """
    if current_question_id is None:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1

    # let's check if there is more questions
    if next_question_id < len(PYTHON_QUESTION_LIST):
        question_data = PYTHON_QUESTION_LIST[next_question_id]
        
        question_text = question_data['question_text']
        options_text = "\n".join([f"{key}) {value}" for key, value in question_data['options'].items()])
        
        formatted_question = f"{question_text}\n{options_text}"
        
        return formatted_question, next_question_id
    else:
        return None, None


def generate_final_response(session):
    """
    creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    """
    user_answers = session.get('user_answers', [])
    score = 0

    for ans in user_answers:
        question_id = ans['question_id']
        user_answer = ans['user_answer']
        correct_answer = PYTHON_QUESTION_LIST[question_id]['answer']
        if user_answer == correct_answer:
            score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    
    session.flush()
    
    return f"Quiz finished! You scored {score} out of {total_questions}."

from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id and current_question_id != 0:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        bot_responses.append(error)
        question_text, _ = get_next_question(current_question_id - 1 if current_question_id is not None else None)
        if question_text:
            bot_responses.append(question_text)
        return bot_responses

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the answer for the current question to django session.
    """
    if current_question_id is None:
        return True, ""

    if 'user_answers' not in session:
        session['user_answers'] = []

    question = PYTHON_QUESTION_LIST[current_question_id]
    
    if answer.lower() not in question['options']:
        error_message = f"Invalid option '{answer}'. Please choose from the available options."
        return False, error_message

    session['user_answers'].append({
        "question_id": current_question_id,
        "user_answer": answer.lower()
    })
    
    return True, ""


def get_next_question(current_question_id):
    """
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    """
    if current_question_id is None:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        question_data = PYTHON_QUESTION_LIST[next_question_id]
        
        question_text = question_data['question_text']
        options_text = "\n".join([f"{key}) {value}" for key, value in question_data['options'].items()])
        
        formatted_question = f"{question_text}\n{options_text}"
        
        return formatted_question, next_question_id
    else:
        return None, None


def generate_final_response(session):
    """
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    """
    user_answers = session.get('user_answers', [])
    score = 0

    for ans in user_answers:
        question_id = ans['question_id']
        user_answer = ans['user_answer']
        correct_answer = PYTHON_QUESTION_LIST[question_id]['answer']
        if user_answer == correct_answer:
            score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    
    session.flush()
    
    return f"Quiz finished! You scored {score} out of {total_questions}."