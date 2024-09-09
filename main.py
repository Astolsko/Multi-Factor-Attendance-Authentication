import flet as ft
from main_api import*
import firebase_admin
from firebase_admin import credentials, firestore
import os

def main(page: ft.Page):
    page.title = "NIT DELHI"
    page.theme_mode = ft.ThemeMode.LIGHT
    email = ft.TextField(hint_text="Username...", width=300, border_radius=20, bgcolor = ft.colors.PRIMARY_CONTAINER)
    password = ft.TextField(hint_text="Password...", width=300, border_radius=20, password=True, bgcolor = ft.colors.PRIMARY_CONTAINER)
    page.theme = ft.Theme(color_scheme_seed="blue")
    code = ft.TextField(label = "Course Code")

    #FACULTY MAIN
    def faculty_main_nav(e):
        selected_index = e.control.selected_index

        if selected_index == 0:
            def qr_butt(e):
                date, time = get_date_time()
                location = get_location()
                course_code = code.value
                print(username)
                generate_and_save_qr_code(course_code, date, time, location, username)
                qr = ft.Image(src = f"qr_code.png", height = 500, width = 500)
                c.controls.append(qr)
                c.controls.append(ft.Text(course_code, size=28))
                code.value = ""
                page.update()
            c = ft.Column(
                [
                    ft.Row(

                        [
                            ft.Container(height = 100),
                            code,
                            ft.ElevatedButton("Generate", on_click = qr_butt)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                expand=True,
                spacing = 50,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        
            r.controls[:] = r.controls[0:1]
            r.controls.append(c)
                    
                    #ft.Container(height=20),
                    #ft.Text("Content for QR Code"),
        elif selected_index == 1:
            courses = display_courses(username)
            selected_course = None
            def close_anchor_1(e):
                text = f"{e.control.data}"
                selected_course  = text
                print(f"closing view from {text}")
                anchor_1.close_view(text)

            def handle_submit_1(e):
                print(f"handle_submit e.data: {e.data}")
                selected_course = e.data
                dates = display_dates(selected_course, username)
                def close_anchor_2(e):
                    text = f"{e.control.data}"
                    selected_course  = text
                    print(f"closing view from {text}")
                    anchor_2.close_view(text)

                def handle_submit_2(e):
                    selected_date = e.data
                    table_data=display_attendance(selected_course, selected_date, username)
                    table = ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Name")),
                            ft.DataColumn(ft.Text("Date")),
                            ft.DataColumn(ft.Text("Time")),
                        ],
                    )
                    for x in table_data:
                        table.rows.append(
                            ft.DataRow(
                                cells = [
                                    ft.DataCell(ft.Text(x[i]))
                                    for i in range(0,3)
                                ],
                            ),
                        )
                    c3 = ft.Column(
                        [
                            ft.Container(height = 50),
                            ft.Container(
                                margin=10,
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                expand = True,
                                padding=10,
                                border_radius=10,
                                content = ft.Column(
                                    [
                                        table
                                    ],
                                    expand=True,
                                    scroll=ft.ScrollMode.ALWAYS
                                )
                            )
                        ],
                        
                    )
                    r.controls[:] = r.controls[0:3]
                    r.controls.append(ft.Container(width = 50))
                    r.controls.append(c3)
                    page.update()

                anchor_2 = ft.SearchBar(
                    view_elevation=4,
                    divider_color=ft.colors.SURFACE_VARIANT,
                    bar_hint_text="Search Dates...",
                    view_hint_text="Choose a Date from the suggestions...",
                    #on_change=handle_change,
                    on_submit=handle_submit_2,
                    #on_tap=handle_tap_2,
                     controls=[
                        ft.ListTile(title=ft.Text(f"{x}"), on_click=close_anchor_2, data=x)
                        for x in dates                                  
                    ],
                    width = 300,
                )
                c1.controls = c1.controls[:4]
                c1.controls.append(ft.Container(height = 100))
                c1.controls.append(ft.Text("Press Enter To Select", size = 20, color = ft.colors.BLUE)),
                c1.controls.append(anchor_2)
                page.update()
                

            def handle_tap_1(e):
                print(f"handle_tap")

            anchor_1 = ft.SearchBar(
                            view_elevation=4,
                            divider_color=ft.colors.SURFACE_VARIANT,
                            bar_hint_text="Search Courses...",
                            view_hint_text="Choose a Course Code from the suggestions...",
                            #on_change=handle_change,
                            on_submit=handle_submit_1,
                            on_tap=handle_tap_1,
                            width = 300,
                            controls=[
                                ft.ListTile(title=ft.Text(f"{x}"), on_click=close_anchor_1, data=x)
                                for x in courses                                   
                            ],
                        )
            
            c1 = ft.Column(
                [
                    ft.Text("Press Enter To Select", size = 20, color = ft.colors.BLUE),
                    ft.Container(height = 10),
                    anchor_1
                ],
            )
            c2 = ft.Column(
                [
                    ft.Container(height  =20),
                    c1
                ],

            )
            r.controls[:] = r.controls[0:1]
            r.controls.append(c2)
        elif selected_index == 2:
            courses = display_courses(username)

            def close_anchor(e):
                text = f"{e.control.data}"
                selected_course  = text
                print(f"closing view from {text}")
                anchor.close_view(text)
            
            def handle_submit(e):
                text = f"{e.control.data}"
                selected_course  = e.data
                print(selected_course)
                attendance_counts = display_total_attendance(username, selected_course)
                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Name")),
                        ft.DataColumn(ft.Text("Total Attendance")),
                    ],
                )
                for x in attendance_counts:
                    table.rows.append(
                        ft.DataRow(
                            cells = [
                                ft.DataCell(ft.Text(x)),
                                ft.DataCell(ft.Text(attendance_counts[x]))
                            ]
                        )
                    )
                table_container = ft.Container(
                    expand=True,
                    margin=10,
                    padding=10,
                    border_radius=10,
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    content = ft.Column(
                        [
                            table
                        ],
                        expand=True,
                        scroll=ft.ScrollMode.ALWAYS
                    )
                )

                c3.controls= c3.controls[0:3]
                c3.controls.append(ft.Container(width = 50))
                c3.controls.append(table_container)
                page.update()

            anchor = ft.SearchBar(
                        view_elevation=4,
                        divider_color=ft.colors.SURFACE_VARIANT,
                        bar_hint_text="Search Courses...",
                        view_hint_text="Choose a Course Code from the suggestions...",
                        #on_change=handle_change,
                        on_submit=handle_submit,
                        #on_tap=handle_tap,
                        width = 300,
                        controls=[
                            ft.ListTile(title=ft.Text(f"{x}"), on_click=close_anchor, data=x)
                            for x in courses                                   
                        ],
                    )
            c3 = ft.Column(
                [
                    ft.Text("Press Enter To Select", size = 20, color = ft.colors.BLUE),
                    ft.Container(height = 50),
                    anchor
                ],
                expand=True
            )
            r.controls[:] = r.controls[0:1]
            r.controls.append(c3)
            page.update()
        elif selected_index == 3:
            page.go("/")
        page.update()

    r = ft.Row(
        [
            ft.NavigationRail(
                selected_index=0,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width = 100,
                min_extended_width=400,
                group_alignment=-0.7,
                elevation = 30,
                on_change=faculty_main_nav,
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.icons.QR_CODE,
                        label="Generate QR",
                        padding = 20
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.ASSESSMENT,
                        label="Show Attendance",
                        padding = 20
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.SCHOOL,
                        label="Total Attendance",
                        padding = 20
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.LOGOUT,
                        label="Log Out",
                        padding = 20
                    ),
                ],
                bgcolor=ft.colors.PRIMARY_CONTAINER
            )              
        ],
        expand = True,
        spacing = 50,
    )

    #ADMIN MAIN
    def admin_main_nav(e):
        selected_index = e.control.selected_index
        #delete bachi
        if selected_index == 0:
            def close_anchor(e):
                text = f"{e.control.data}"
                selected_course  = text
                print(f"closing view from {text}")
                student_searchbar.close_view(text)
            
            def handle_student_submit(e):
                selected_student=e.data
                
                def close_dlg(e):
                    dlg_modal.open = False
                    page.update()
                def open_dlg_modal(e):
                    page.dialog = dlg_modal
                    dlg_modal.open = True
                    page.update()
                def delete_stu(e):
                    def open_dlg(e):
                        page.dialog = dlg
                        dlg.open = True
                        page.update()
                    deleted = delete_student_user(selected_student)
                    if deleted == -1:
                        dlg = ft.AlertDialog(
                            title=ft.Text("User Not Found")
                        )
                        open_dlg(e)
                    else:
                        dlg = ft.AlertDialog(
                            title=ft.Text("User Deleted Successfully")
                        )
                        open_dlg(e)

                dlg_modal = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Please confirm"),
                    content=ft.Text("Do you really want to delete this student"),
                    actions=[
                        ft.TextButton("Yes", on_click=delete_stu),
                        ft.TextButton("No", on_click=close_dlg),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    #on_dismiss=lambda e: print("Modal dialog dismissed!"),
                )

                open_dlg_modal(e)

            students = display_student_users()
            student_searchbar = ft.SearchBar(
                view_elevation=4,
                divider_color=ft.colors.ON_PRIMARY,
                view_bgcolor= ft.colors.ON_PRIMARY,
                bar_hint_text="Select student",
                view_hint_text="Choose a student from the suggestions...",
                #on_change=handle_change,
                on_submit=handle_student_submit,
                #on_tap=handle_tap_1,
                width = 300,
                controls=[
                    ft.ListTile(title=ft.Text(f"{x}"), on_click=close_anchor, data=x)
                    for x in students                                
                ],
            )
            contain = ft.Container(
                margin=10,
                padding=100,
                alignment=ft.alignment.Alignment(-0.5, -0.5),
                border_radius=10,
                height=500,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                content=ft.Column(
                [
                    ft.Text("Press Enter To Select", size = 20, color = ft.colors.BLUE),
                    ft.Container(height = 30),
                    student_searchbar
                ],
                )
            )
            content_row = ft.Row(
                [
                    contain
                ],
                alignment= ft.MainAxisAlignment.CENTER,
                expand = True
            )

            roww.controls[:] = roww.controls[0:1]
            roww.controls.append(content_row)
            page.update()
        
        #add faculty:
        if selected_index == 1:

            def add_faculty(e):
                faculty_name.error_text = ""
                faculty_username.error_text = ""
                faculty_password.error_text = ""

                if not faculty_name.value:
                    faculty_name.error_text = "Missing Name"
                    page.update()
                elif not faculty_username.value:
                    faculty_username.error_text = "Missing Username"
                    page.update()
                elif not faculty_password.value:
                    faculty_password.error_text = "Missing Password"
                    page.update()
                else:
                    def open_dlg(e):
                        page.dialog = dlg
                        dlg.open = True
                        page.update()
                    add_faculty_user(faculty_name.value, faculty_username.value, faculty_password.value)
                    dlg = ft.AlertDialog(
                            title=ft.Text("Faculty User Added Successfully")
                    )
                    open_dlg(e)
                    faculty_name.value = ""
                    faculty_username.value = ""
                    faculty_password.value = ""
                    page.update()


            faculty_name = ft.TextField(hint_text="Name...", width=300, border_radius=20, bgcolor = ft.colors.ON_SECONDARY)
            faculty_username= ft.TextField(hint_text="Username...", width=300, border_radius=20, bgcolor = ft.colors.ON_SECONDARY)
            faculty_password = ft.TextField(hint_text="Password...", width=300, border_radius=20, password=True, bgcolor = ft.colors.ON_SECONDARY)

            button = ft.ElevatedButton("Submit", on_click=add_faculty)
            container = ft.Container(
                margin=10,
                padding=50,
                border_radius=10,
                height=500,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                content=ft.Column(
                    [
                    ft.Container(height = 10),
                    faculty_name,
                    ft.Container(height = 10),
                    faculty_username,
                    ft.Container(height = 10),
                    faculty_password,
                    ft.Container(height = 10),
                    button
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )


            secondary_row = ft.Row(
                [
                    container
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                expand = True
            )

            roww.controls[:] = roww.controls[0:1]
            roww.controls.append(secondary_row)
            page.update()

        #delete Faculty
        if selected_index == 2:
            def close_anchor(e):
                text = f"{e.control.data}"
                selected_course  = text
                print(f"closing view from {text}")
                faculty_searchbar.close_view(text)
            
            def handle_faculty_submit(e):
                selected_faculty=e.data
                
                def close_dlg(e):
                    dlg_modal.open = False
                    page.update()
                def open_dlg_modal(e):
                    page.dialog = dlg_modal
                    dlg_modal.open = True
                    page.update()
                def delete_fac(e):
                    def open_dlg(e):
                        page.dialog = dlg
                        dlg.open = True
                        page.update()
                    deleted = delete_faculty(selected_faculty)
                    if deleted == -1:
                        dlg = ft.AlertDialog(
                            title=ft.Text("User Not Found")
                        )
                        open_dlg(e)
                    else:
                        dlg = ft.AlertDialog(
                            title=ft.Text("User Deleted Successfully")
                        )
                        open_dlg(e)

                dlg_modal = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Please confirm"),
                    content=ft.Text("Do you really want to delete this faculty"),
                    actions=[
                        ft.TextButton("Yes", on_click=delete_fac),
                        ft.TextButton("No", on_click=close_dlg),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    #on_dismiss=lambda e: print("Modal dialog dismissed!"),
                )

                open_dlg_modal(e)

            faculty = display_faculty_users()
            faculty_searchbar = ft.SearchBar(
                view_elevation=4,
                divider_color=ft.colors.SURFACE_VARIANT,
                bar_hint_text="Select Faculty",
                view_hint_text="Choose a Faculty from the suggestions...",
                #on_change=handle_change,
                on_submit=handle_faculty_submit,
                #on_tap=handle_tap_1,
                width = 300,
                controls=[
                    ft.ListTile(title=ft.Text(f"{x}"), on_click=close_anchor, data=x)
                    for x in faculty                              
                ],
            )


            main_container = ft.Container(
                margin=10,
                padding=100,
                alignment=ft.alignment.Alignment(-0.5, -0.5),
                border_radius=10,
                height=500,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                content= ft.Column(
                    [
                    ft.Text("Press Enter To Select", size = 20, color = ft.colors.BLUE),
                    ft.Container(height = 10),
                    faculty_searchbar
                    ],
                )
            )
            sec_row = ft.Row(
                [
                    main_container
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
            )
            
            roww.controls[:] = roww.controls[0:1]
            roww.controls.append(sec_row)
            page.update()

        #Add Admin User
        if selected_index == 3:
            def add_admin(e):
                admin_name.error_text = ""
                admin_username.error_text = ""
                admin_password.error_text = ""

                if not admin_name.value:
                    admin_name.error_text = "Missing Name"
                    page.update()
                elif not admin_username.value:
                    admin_username.error_text = "Missing Username"
                    page.update()
                elif not admin_password.value:
                    admin_password.error_text = "Missing Password"
                    page.update()
                else:
                    def open_dlg(e):
                        page.dialog = dlg
                        dlg.open = True
                        page.update()
                    added  = add_admin_user(admin_username.value, admin_name.value, admin_password.value)
                    if added == -1:
                        dlg = ft.AlertDialog(
                                title=ft.Text("Admin User Already Exists")
                        )
                        open_dlg(e)
                    else:
                        dlg = ft.AlertDialog(
                                title=ft.Text("Admin User Added Successfully")
                        )
                        open_dlg(e)

                    admin_name.value = ""
                    admin_username.value = ""
                    admin_password.value = ""
                    page.update()


            admin_name = ft.TextField(hint_text="Name...", width=300, border_radius=20, bgcolor = ft.colors.ON_SECONDARY)
            admin_username= ft.TextField(hint_text="Username...", width=300, border_radius=20, bgcolor = ft.colors.ON_SECONDARY)
            admin_password = ft.TextField(hint_text="Password...", width=300, border_radius=20, password=True, bgcolor = ft.colors.ON_SECONDARY)

            button = ft.ElevatedButton("Submit", on_click=add_admin)

            primary_container = ft.Container(
                margin=10,
                padding=50,
                border_radius=10,
                height=500,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                content=ft.Column(
                    [
                    ft.Container(height = 10),
                    admin_name,
                    ft.Container(height = 10),
                    admin_username,
                    ft.Container(height = 10),
                    admin_password,
                    ft.Container(height = 10),
                    button
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            sec_row = ft.Row(
                [
                    primary_container
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                expand = True
            )

            roww.controls[:] = roww.controls[0:1]
            roww.controls.append(sec_row)
            page.update()

        if selected_index == 4:

            def del_admin(e):
                admin_name.error_text = ""
                admin_password.error_text = ""

                if not admin_name.value:
                    admin_name.error_text = "Missing Name"
                    page.update()
                elif not admin_password.value:
                    admin_password.error_text = "Missing Password"
                    page.update()
                else:
                    def close_dlg(e):
                        dlg_modal.open = False
                        page.update()
                    def open_dlg_modal(e):
                        page.dialog = dlg_modal
                        dlg_modal.open = True
                        page.update()
                    def delete_adm(e):
                        def open_dlg(e):
                            page.dialog = dlg
                            dlg.open = True
                            page.update()
                        deleted = delete_admin_user(admin_name.value, admin_password.value)
                        if deleted == -1:
                            admin_password.error_text="Wrong Password"
                            page.update()
                        elif deleted == -2:
                            dlg = ft.AlertDialog(
                                title=ft.Text("Admin User Not Found")
                            )
                            open_dlg(e)
                        else:
                            dlg = ft.AlertDialog(
                                title=ft.Text("Admin User Deleted Successfully")
                            )
                            open_dlg(e)
                            admin_name.value = ""
                            admin_password.value = ""
                            page.update()

                    dlg_modal = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Please confirm"),
                        content=ft.Text("Do you really want to delete this user"),
                        actions=[
                            ft.TextButton("Yes", on_click=delete_adm),
                            ft.TextButton("No", on_click=close_dlg),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                        #on_dismiss=lambda e: print("Modal dialog dismissed!"),
                    )

                    open_dlg_modal(e)
            admin_name= ft.TextField(hint_text="Username...", width=300, border_radius=20, bgcolor = ft.colors.ON_SECONDARY)
            admin_password = ft.TextField(hint_text="Password...", width=300, border_radius=20, password=True, bgcolor = ft.colors.ON_SECONDARY)

            button = ft.ElevatedButton("Submit", on_click=del_admin)

            primary_container_1 = ft.Container(
                margin=10,
                padding=50,
                border_radius=10,
                height=500,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                content=ft.Column(
                    [
                    ft.Container(height = 10),
                    admin_name,
                    ft.Container(height = 10),
                    admin_password,
                    ft.Container(height = 10),
                    button
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
            secondary_row_1 = ft.Row(
                [
                    primary_container_1
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                expand = True
            )

            roww.controls[:] = roww.controls[0:1]
            roww.controls.append(secondary_row_1)
            page.update()

        if selected_index == 5:
            roww.controls[:] = roww.controls[0:1]
            page.update()

            def close_dlg(e):
                dlg_modal.open = False
                page.update()
            def open_dlg_modal(e):
                page.dialog = dlg_modal
                dlg_modal.open = True
                page.update()

            def clear(e):
                clear_data()
                close_dlg(e)

            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Do you really want to clear all data"),
                actions=[
                    ft.TextButton("Yes", on_click=clear),
                    ft.TextButton("No", on_click=close_dlg),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                #on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )
            open_dlg_modal(e)
            
        if selected_index == 6:
            page.go("/")


    roww = ft.Row(
        [
            ft.NavigationRail(
                selected_index=0,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width = 150,
                min_extended_width=400,
                group_alignment=-0.7,
                elevation = 30,
                on_change=admin_main_nav,
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.icons.PERSON_REMOVE,
                        label="Delete student",
                        padding = 15
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.PERSON_ADD,
                        label="Add faculty",
                        padding = 15
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.PERSON_REMOVE,
                        label="Delete faculty",
                        padding = 15
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.PERSON_ADD,
                        label="Add admin",
                        padding = 15
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.PERSON_REMOVE,
                        label="Remove admin",
                        padding = 15
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.CLEAR_ALL_OUTLINED,
                        label="Clear data",
                        padding = 15
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.LOGOUT_OUTLINED,
                        label="Logout",
                        padding = 15
                    ),
                ],
                #extended=True,
                #expand = True
                bgcolor=ft.colors.PRIMARY_CONTAINER
            )              
        ],
        expand = True,
        spacing = 50,
        #alignment=ft.MainAxisAlignment.CENTER
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
            "/",
            [
                ft.AppBar(title = ft.Text('Login'), bgcolor = ft.colors.SURFACE_VARIANT),
                ft.Image(src = f"images/profile_img.png", height = 100, width = 100),
                ft.Container(height=20),
                ft.Text("Choose Your Account Type", size  = 20, weight = 20),
                ft.Container(height=10),
                ft.Row(
                controls = [
                    ft.ElevatedButton("Faculty", on_click=lambda _: page.go("/faculty_login")),
                    ft.ElevatedButton("Admin", on_click=lambda _: page.go("/Admin"))
                ],
                alignment='center'
                )
            ],
            scroll = "always",
            vertical_alignment = "center",
            horizontal_alignment = "center",
            padding = 100,
            
            )
        )
        page.theme  = ft.Theme(color_scheme_seed='blue')
        

        if page.route == '/faculty_login':
            page.views.append(
                ft.View(
                    "/faculty_login",
                    [
                        ft.AppBar(title = ft.Text('Faculty Login'), bgcolor = ft.colors.SURFACE_VARIANT),
                        email,
                        password,
                        ft.Container(height=20),
                        ft.ElevatedButton("Login", on_click = email_pass_verification_faculty),
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center",
                    padding=100,
                )
            )
            page.theme  = ft.Theme(color_scheme_seed='blue')

        if page.route == '/Admin':
            page.views.append(
                ft.View(
                    "/Admin",
                    [
                        ft.AppBar(title = ft.Text('Admin'), bgcolor = ft.colors.SURFACE_VARIANT),
                        email,
                        password,
                        ft.Container(height=20),
                        ft.ElevatedButton("Login", on_click = email_pass_verification_admin),
                    ],
                    scroll="always",
                    vertical_alignment="center",
                    horizontal_alignment="center",
                    padding=100,
                )
                
            )
            page.theme  = ft.Theme(color_scheme_seed='blue')
        
        if page.route == '/faculty_main':
            page.views.append(
                ft.View(
                    "/faculty_main",
                    [
                        r
                    ],
                    #scroll="always",
                    padding = 20
                )
            )
            page.theme  = ft.Theme(color_scheme_seed='blue')

        if page.route == '/admin_main':
            page.views.append(
                ft.View(
                    "/admin_main",
                    [
                        roww
                    ],
                    #scroll="always",
                    padding = 20
                )
            )
            page.theme  = ft.Theme(color_scheme_seed='blue')
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
               
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    def email_pass_verification_faculty(e):
        email.error_text = ""
        password.error_text = ""
        if not email.value:
            email.error_text = "Missing email"
            page.update()
        elif not password.value:
            password.error_text = "Missing password"
            page.update()
        else:
            if validate_user_faculty(email.value , password.value):
                print(email.value)
                global username
                username = email.value
                page.go("/faculty_main")
            else: 
                password.error_text = "wrong password or email"
                page.update()
    
    def email_pass_verification_admin(e):
        email.error_text = ""
        password.error_text = ""
        if not email.value:
            email.error_text = "Missing email"
            page.update()
        elif not password.value:
            password.error_text = "Missing password"
            page.update()
        else:
            if validate_user_admin(email.value , password.value):
                page.go("/admin_main")
                global username
                username=email.value
            else: 
                password.error_text = "wrong password or email"
                page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, assets_dir="assets")