# Course_Exhange
This is the project I work for college's python programming course as final report. The idea came from one time I chat with my friend, and found out many student in NTUST have trouble to register or exchange desire course. So, I use the knowledge from  python course to write a simple UI interface for students to exchage course. And since the possible exchange path sometimes could be complicated,  involving more than 2 students. I use the idea from algorithm course to write a DFS-modify algorithm to check all the possible case.

## DFS-modify Algorithm
In the algorithm, I use nodes as courses and edge as student's exchange-wish which contain data such as student name, wish_course and give_course. Then, the possible exchange path will be clear, it is just the path which start from user's give_course and all the way back to the node again. As a result, I can modify DFS algorithm, to run all the node in exchange graph effectively, and record all the possible exchanging path. 

## Test Result
I test the algorithm on simple 5 courses, 7 students and 7 course exchange scenario. And it successfully show all the possible exchange case for every students.

## Future Development
The project is currently only build for self-test. I will use the algorithm to write a website which will allow student to enroll and exchange courses.