from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

class User:
    def __init__(self, name):
        self.name = name
        self.edges = []
    def add_edge(self, edge):
        self.edges.append(edge)
    def __str__(self):
        return "{}".format(self.name)
    
class Edge:
    def __init__(self, user, change, want):
        self.user = user
        self.change = change
        self.want = want
    def __str__(self):
        return "User {} : {} -> {}".format(self.user, self.change, self.want)

class Course:
    def __init__(self, name):
        self.name = name
        self.OutEdge = [] # Using course to change
        self.InEdge = [] # Want this course
    def add_InEdge(self, edge):
        self.InEdge.append(edge)
    def add_OutEdge(self, edge):
        self.OutEdge.append(edge)
    def __str__(self):
        return "{}".format(self.name)

class graph:
    def __init__(self):
        self.courses = []
        self.user = []
    def add_user(self, name):
        user = User(name)
        self.user.append(user)
        return user
    def add_course(self, course_name):
        self.courses.append(Course(course_name))
    def add_edge(self, user_name, own_coures_name, want_course_name):
        # first, check whether user and courses are exist in graph or not
        try :
            user = self.find_user(user_name)
        except NameError:
            raise
        try :
            own_course = self.__find_course(own_coures_name)
        except NameError:
            raise
        try :
            want_course = self.__find_course(want_course_name)
        except NameError:
            raise
        # if they all exist, add a new edge between two courses
        edge = Edge(user, own_course, want_course)
        own_course.add_OutEdge(edge)
        want_course.add_InEdge(edge)
        user.add_edge(edge)
    # if the givne course_name is not exist in self.course, raise NameError
    def __find_course(self, course_name):
        for course in self.courses:
            if course_name == course.name:
                return course
        raise NameError
    # if the given user_name is not exist in self.user, raise NameError
    def find_user(self, user_name):
        for user in self.user:
            if user.name == user_name:
                return user
        raise NameError
    # match_course is an algorithms to find all the possible ways to change the course
    def match_course(self, own_course, want_course, edges, edge_set, visited):
        new_edges = []
        new_edges += edges
        # using visited list to record all the course that had been checked
        visited.append(want_course)
        for edge in want_course.OutEdge:
            new_edges.append(edge)
            next_course = edge.want
            # only when the course is not visited before, the algorithms will check it
            if next_course not in visited:
                # if the edge connected to original course, it means the algorithms
                # find a possible path to change the courses
                if next_course == own_course:
                    edge_set.append(new_edges)
                # otherwise, keep checking by recursivly call the match_course
                else :
                    new_edge_set = self.match_course(own_course, next_course, new_edges, edge_set, visited)
                    # only when the new set is been changed, the edge_set will be replaced
                    if new_edge_set != edge_set:
                        edge_set += new_edge_set
            new_edges = []
            new_edges += edges
        return edge_set
        
if __name__ == '__main__':
    # Create a graph for new task
    G = graph()
    # When add_course_btn is clicked, this function will trigger and show result
    def add_course_clicked():
        course_name = course_txt.get()
        # if course name is not type in, it will raise a window to show the error
        if course_name == "":
            messagebox.showinfo("Error","Course name is required!")
        else :
            # add course into graph
            G.add_course(course_name)
            messagebox.showinfo("Added!", "{} is added!".format(course_name))
    # when add_user_btn is clicked, this funcion will trigger and show result
    def add_user_clicked():
        user_name = user_txt.get()
        # if user's name is not type in, it will raise an error
        if user_name == "":
            messagebox.showinfo("Error", "User name is required!")
        else :
            # add user into the graph
            G.add_user(user_name)
            messagebox.showinfo("Added!", "{} is added!".format(user_name))
    # when add_requirement's btn is clicked, this fuction will trigger and show result 
    def add_edge_clicked():
        user = requ_user_txt.get()
        own_course = requ_own_c_txt.get()
        want_course = requ_want_c_txt.get() 
        # if any filed is not type in, it will raise an error
        if (user == "") or (own_course == "") or (want_course == ""):
            messagebox.showinfo("Error", "Every fields have to be filled!")
        else :
            # only when G.add_edge can find user and courses, the function will work
            try :
                G.add_edge(user, own_course, want_course)
                messagebox.showinfo("Error", "Add requirement!")
            # otherwise, it will raise an error
            except NameError:
                messagebox.showinfo("Error", "User or Course do not exist!")
    # when match_btn is clicked, this function will trigger and show result window
    def match_clicked():
        user_name = match_txt.get()
        if user_name == "":
            messagebox.showinfo("Error!", "User does not exist!")
        else :
            # try the following procedure only when the user exists
            try :
                user = G.find_user(user_name)
                # create a new window to show the result
                result = Tk()
                result.title("Possible changing path")
                # using two index to record the current position in window
                row_index = 0
                column_index = 0
                # using this parameter to record whether any result is printed out
                print_or_not = False
                # Check every requirement the given user had
                for edge in user.edges:
                    print_or_not = True
                    own_course = edge.change
                    want_course = edge.want
                    # Show which requirment is checked now
                    info_lbl = Label(result, text="For {} : {} -> {}".format(user.name, own_course.name, want_course.name))
                    info_lbl.grid(column=column_index, row=row_index)
                    row_index += 1
                    # using graph's match_course function to find every possible paths
                    edge_set = G.match_course(own_course, want_course, [edge], [], [])
                    index = 1
                    # print every possible paths
                    for edges in edge_set:
                        # only print out those under path distance
                        if len(edges) <= int(match_distance.get()):
                            info_lbl = Label(result, text="{} : ".format(str(index)))
                            info_lbl.grid(column=column_index, row=row_index)
                            row_index += 1
                            for edge in edges:
                                info_lbl = Label(result, text="User {} use {} change {}".format(
                                        edge.user.name, edge.change.name, edge.want.name))
                                info_lbl.grid(column=column_index, row=row_index)
                                row_index += 1
                            index += 1
                    # if index is still 1, it means there's no availble way to change course
                    if index == 1:
                        info_lbl = Label(result, text="No path is available !")
                        info_lbl.grid(column=column_index, row=row_index)
                        row_index += 1
                # if print_or_not is still False, it means no requirement in given User
                if not print_or_not :
                    info_lbl = Label(result, text="No requirement yet!")
                    info_lbl.grid(column=column_index, row=row_index)
            except NameError:
                messagebox.showinfo("Error!", "User does not exist!")

    window = Tk()
    window.title("Course Exchange System")
    window.geometry('600x800')
    # Create all the Labels in window
    add_course_lbl = Label(window, text="Add Course : ")
    add_user_lbl = Label(window, text="Add User : ")
    add_requirement_lbl = Label(window, text="Add requirement : ")
    requ_user_lbl = Label(window, text="User : ")
    requ_own_c_lbl = Label(window, text="Own Course : ")
    requ_want_c_lbl = Label(window, text="Want Course : ")
    match_lbl = Label(window, text="Match for User : ")
    # Create all the Enties in window 
    course_txt = Entry(window, width=10)
    user_txt = Entry(window, width=10)
    requ_user_txt = Entry(window, width=5)
    requ_own_c_txt = Entry(window, width=15)
    requ_want_c_txt = Entry(window, width=15)
    match_txt = Entry(window, width=10)
    # Create all the Buttons in window
    add_course_btn = Button(window, text="Add", command=add_course_clicked)
    add_user_btn = Button(window, text="Add", command=add_user_clicked)
    add_requ_btn = Button(window, text="Add", command=add_edge_clicked)
    match_btn = Button(window, text="Match", command=match_clicked)
    # Create all the Combo box in window
    match_distance = Combobox(window, width=3)
    match_distance['values'] = (1, 2, 3, 4, 5, 6)
    # Grid every element in window
    add_course_lbl.grid(column=0, row=0)
    course_txt.grid(column=1, row=0)
    add_course_btn.grid(column=2, row=0)
    add_user_lbl.grid(column=0, row=1)
    user_txt.grid(column=1, row=1)
    add_user_btn.grid(column=2, row=1)
    add_requirement_lbl.grid(column=1, row=3)
    requ_user_lbl.grid(column=0, row=4)
    requ_user_txt.grid(column=1, row=4)
    requ_own_c_lbl.grid(column=0, row=5)
    requ_own_c_txt.grid(column=1, row=5)
    requ_want_c_lbl.grid(column=0, row=6)
    requ_want_c_txt.grid(column=1, row=6)
    add_requ_btn.grid(column=2, row=6)
    match_lbl.grid(column=0, row=9)
    match_txt.grid(column=1, row=9)
    match_distance.grid(column=2, row=9)
    match_btn.grid(column=3, row=9)
    window.mainloop()