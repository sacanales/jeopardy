from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Define categories and questions with explanations
categories = {
    "Epidemiology": {
        100: ("A 32-year-old G2P1 woman presents to labor and delivery at 37 weeks gestation. She reports the rupture of membranes 2 hours ago. She has not received any prenatal care. Given her situation, identify the key factor from her history that would increase her newborn's risk for this infectious condition.", "What is lack of prenatal care increasing the risk for Group B Streptococcus (GBS) disease?", "The vignette describes a situation where a pregnant woman has not received any prenatal care and reports premature rupture of membranes at 37 weeks gestation. Lack of prenatal care is a significant risk factor for neonatal GBS disease because it means the mother has likely not been screened for GBS colonization during the third trimester, as is recommended. Therefore, the absence of prenatal care directly impacts the newborn's risk for GBS infection, particularly early-onset disease, which can occur in the first week of life."),
        
        200: ("A newborn is diagnosed with late-onset GBS disease at 5 weeks of age. The mother recalls being told her GBS status was negative during pregnancy. Considering the age of onset, what is a significant risk factor for this type of GBS disease presentation?", "What is horizontal transmission from caregivers or environmental sources?", "The highlighted risk factor in this scenario, horizontal transmission from caregivers or environmental sources, refers to the acquisition of GBS after birth from contacts or surroundings, rather than directly from the mother at the time of delivery. Caregivers, including family members, healthcare workers, or others who have close contact with the infant, can inadvertently transmit GBS bacteria to the child through direct contact. Environmental sources can also harbor GBS, although less commonly, and lead to neonatal infection."),
        
        300: ("A neonatologist is reviewing the case of a term neonate admitted with late-onset GBS meningitis. The infants mother was GBS-negative at 36 weeks gestation, and the delivery was uncomplicated. Which environmental or postnatal factor is increasingly recognized as a potential risk for late-onset GBS disease in neonates, highlighting the complexity of transmission routes beyond maternal vertical transmission?", "What is horizontal transmission from hospital or community contacts?", "Late-onset GBS disease, which occurs between 7 days and 3 months of age, can be attributed to horizontal transmission from sources other than the mother, including hospital staff, family members, or other community contacts. This emphasizes the importance of hygiene practices in the care of newborns and demonstrates that GBS infection can occur via multiple pathways, not exclusively through maternal vertical transmission. Understanding and addressing these additional risk factors are crucial for preventing late-onset GBS disease."),
        
        400: ("Identify a population-based risk factor for infectious diseases in newborns.", "Maternal infection", "Maternal infections can be passed to the newborn during delivery."),
    },
    "Prevention and Screening": {
        100: ("A 28-year-old pregnant woman at 35 weeks gestation is found to have GBS colonization. She is allergic to penicillin with a history of anaphylaxis. Based on her allergy status, which antibiotic should be administered for intrapartum prophylaxis?", "What is clindamycin (if GBS is susceptible) or vancomycin?", "This question focuses on an expectant mother who is known to be colonized with GBS but also has a history of anaphylaxis to penicillin, making the preferred antibiotic choice (penicillin or ampicillin) unsuitable for her. In such cases, alternative antibiotics are considered based on GBS susceptibility. Clindamycin is an option if the GBS strain is susceptible to it. However, if the GBS strain is resistant to clindamycin or if susceptibility cannot be determined, vancomycin becomes the antibiotic of choice for intrapartum prophylaxis."),
        
        200: ("During a routine prenatal visit at 36 weeks gestation, a pregnant woman undergoes screening for GBS. The result is positive. She has no known drug allergies. Given the current guidelines, what is the recommended course of action to prevent early-onset GBS disease in her newborn?", "What is administering intrapartum antibiotic prophylaxis (IAP) with penicillin or ampicillin during labor?", "For pregnant women found to be colonized with GBS during routine screening, the current recommendation to prevent early-onset GBS disease in their newborns is to administer intrapartum antibiotic prophylaxis (IAP) during labor. Penicillin or ampicillin is the preferred treatment due to their efficacy against GBS, low risk of side effects, and ability to reduce the transmission of GBS from mother to baby during the birthing process. Must be given ≥4 hours prior to delivery."),
        
        300: ("A 29-year-old woman at 37 weeks gestation is admitted for labor induction. Her prenatal course was complicated by a positive GBS urine culture at 16 weeks and a penicillin allergy without anaphylaxis. She received an alternative antibiotic treatment for the UTI but is concerned about her baby's risk at delivery. What specific intervention should be provided to minimize the risk of neonatal GBS disease given her allergy status and GBS history?", "What is the administration of cefazolin for intrapartum antibiotic prophylaxis because of the low risk of anaphylaxis in penicillin-allergic patients without a history of anaphylaxis to penicillin?", "In a penicillin-allergic patient without a history of anaphylaxis to penicillin, cefazolin is preferred due to its efficacy and lower risk of cross-reactivity. This approach minimizes neonatal GBS disease risk while considering the maternal allergy status."),
        
        400: ("What prophylactic treatment is recommended for women with positive GBS screening?", "Intrapartum antibiotics", "Antibiotics given during labor can significantly reduce the risk of transmitting GBS to the newborn."),
    },
    "Clinical Manifestations": {
        100: ("A term newborn is noted to be lethargic and feed poorly 24 hours post-delivery. The infant is also observed to have a temperature instability. What is the most important disease to rule out given these clinical manifestations?", "What is early-onset Group B Streptococcus (GBS) sepsis?", "The newborn presented in this vignette displays lethargy, poor feeding, and temperature instability within the first 24 hours after birth, which are concerning signs suggestive of neonatal sepsis. Given the specified timeframe and clinical presentation, early-onset GBS sepsis is a crucial condition to consider and rule out. Early-onset GBS disease, occurring within the first seven days of life, typically presents with signs of systemic infection such as temperature irregularities, respiratory distress, and feeding difficulties. Identifying these symptoms prompts immediate evaluation, including laboratory tests and initiation of empirical antibiotic therapy while awaiting culture results, to manage the condition effectively and mitigate potential complications associated with neonatal sepsis."),
        
        200: ("A 2-month-old infant presents with fever, irritability and a bulging fontanelle. Blood cultures are drawn and an empiric antibiotic course is started. What condition should be strongly considered in the differential diagnosis given the signs and potential exposure history?", "What is late-onset GBS meningitis?", "This clinical scenario describes a 36-hour-old neonate manifesting signs of respiratory distress—grunting, nasal flaring, and retractions—compounded by decreased activity and feeding interest. These symptoms, particularly when observed in a neonate born to a mother with a history of inadequately treated Group B Streptococcus (GBS) colonization, raise substantial concern for early-onset GBS sepsis."),
        
        300: ("A 4-week-old previously healthy infant presents with fever, increased irritability, and a high-pitched cry. Physical examination reveals poor feeding and bulging of the anterior fontanelle upon crying. The infant was delivered at term with an uncomplicated delivery, and the mother reports that she was GBS-negative during prenatal screening. Considering the clinical presentation and the initial negative maternal history for GBS, what significant infectious condition must be ruled out, and what diagnostic procedure is imperative to perform next?", "What is meningitis, necessitating immediate lumbar puncture for cerebrospinal fluid analysis?", "A 4-week-old infant presenting with fever, irritability, poor feeding, and bulging fontanelle, suggestive of increased intracranial pressure, must be evaluated for meningitis. Regardless of initial maternal GBS screening results, meningitis remains a critical consideration in febrile infants with neurological symptoms, and immediate lumbar puncture is necessary for diagnostic cerebrospinal fluid analysis."),
        
        400: ("Which condition is characterized by the abnormal accumulation of fluid in two or more fetal compartments?", "Hydrops fetalis", "Hydrops fetalis can be a complication of infections and other conditions."),
    },
    "Treatment and Management": {
        100: ("A newborn is diagnosed with early-onset GBS disease shortly after birth. The infant's mother was positive for GBS but allergic to penicillin. Considering the newborn's diagnosis and symptoms including respiratory distress and fever, what is the first-line treatment option for this infant?", "What is IV antibiotics, specifically penicillin G or ampicillin plus gentamicin?", "The first-line treatment for a newborn diagnosed with early-onset GBS disease involves the immediate administration of intravenous antibiotics. Penicillin G or ampicillin and Gentamicin (empiric coverage) until the specific causative agent is confirmed."),
        
        200: ("A preterm neonate born at 34 weeks gestation is suspected of having early-onset GBS infection and is started on empiric antibiotics. What two antibiotics should be initially chosen to cover for the most likely pathogens, including GBS?", "What are ampicillin and gentamicin?", "Ampicillin is effective against GBS and other gram-positive organisms, which are common pathogens in neonatal infections. Its broad spectrum also covers certain gram-negative bacteria and Listeria monocytogenes, another critical pathogen in neonates, especially those born prematurely. Gentamicin is added to provide synergistic effects against gram-negative bacteria, enhancing the coverage against a broader range of potential pathogens."),
        
        300: ("A 2-week-old neonate, previously healthy, presents to the pediatric emergency department with a 1-day history of fever, irritability, and decreased oral intake. The infant was born at term following an uncomplicated pregnancy, and the mother's GBS status was negative at 36 weeks gestation. Despite the maternal GBS-negative status, the neonate is diagnosed with late-onset GBS meningitis. After initiating appropriate antibiotic therapy, what critical aspect of supportive care is essential to monitor and potentially adjust in this patient's management plan?", "What is the monitoring and managing of potential complications, such as hydrocephalus or seizures, as part of the comprehensive care for neonatal meningitis?", "An infant diagnosed with late-onset GBS meningitis requires not only appropriate antibiotic therapy but also vigilant supportive care. Monitoring for and managing potential complications, such as seizures and hydrocephalus, are crucial due to the inflammatory responses in the meninges and potential increased intracranial pressure or direct injury to the neural tissue caused by the infection."),
        
        400: ("What is the term for managing newborns with jaundice to prevent kernicterus?", "Phototherapy", "Phototherapy helps reduce bilirubin levels to prevent kernicterus."),
    },
}

@app.before_request
def before_request():
    if request.endpoint == 'game' and 'teams' not in session:
        return redirect(url_for('index'))
    if 'answered_questions' not in session:
        session['answered_questions'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        team1 = request.form.get('team1', 'Team 1')
        team2 = request.form.get('team2', 'Team 2')
        session['teams'] = {team1: 0, team2: 0}
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html', categories=categories, teams=session['teams'], answered_questions=session['answered_questions'])

@app.route('/question/<category>/<int:value>', methods=['GET', 'POST'])
def question(category, value):
    if request.method == 'POST':
        team = request.form['team']
        correct = 'correct' in request.form
        if correct:
            session['teams'][team] += value
            session['answered_questions'].append(f"{category}_{value}")
            session.modified = True
        return redirect(url_for('game'))
    
    question, answer, explanation = categories[category][value]
    return render_template('question.html', category=category, value=value, question=question, answer=answer, explanation=explanation, teams=session['teams'])

if __name__ == '__main__':
    app.run(debug=True)