''' 
Simple MFS Addon Manager
'''
import os
import dearpygui.dearpygui as dpg
import xml.etree.ElementTree as ET
import webbrowser

# PATH EXAMPLE : C:\Users\dadro\AppData\Local\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache 

WINDOWS_CONTENT_XML_PATH = os.getenv('LOCALAPPDATA') + '\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalCache\Content.xml'
STEAM_CONTENT_PATH = os.getenv('LOCALAPPDATA') + '\Microsoft Flight Simulator\LocalCache\Content.xml'

CONTENT_XML = ET.parse(WINDOWS_CONTENT_XML_PATH)
CONTENT_XML_ROOT = CONTENT_XML.getroot() # XML TREE

#os.chdir(r'C:\Users\dadro\Documents\Simple_Addon_Manager')

search_id = 0 # to be filled out later

def get_active_state(pkg_name:str) -> bool:
    for subelem in CONTENT_XML_ROOT.findall('Package'):
        if pkg_name == subelem.get('name'):
            if (subelem.get('active')) == 'true': return True 
            else: return False

def get_total_pkg_status() -> tuple:
    pkg_status = [0, 0]

    for subelem in CONTENT_XML_ROOT.findall('Package'):
        if subelem.get('active') == 'true':
            pkg_status[0] += 1
        else:
            pkg_status[1] += 1
    return pkg_status

def get_search_input(search_id):
    print(dpg.get_value(search_id))


class App:
    def __init__(self, app_title: str, width: int, height: int):
        self.app_title = app_title
        self.width = width
        self.height = height
        dpg.create_context()
        
    def main_window(self):
        width, height, channels, data = dpg.load_image('img\logo.png') # 0: width, 1: height, 2: channels, 3: data
        with dpg.texture_registry():
                dpg.add_static_texture(width, height, data, tag="image_id")

        with dpg.window(label=None, width=self.width, height=self.height, tag="Primary Window"):

            Toolbar()

            dpg.add_separator()

            # ADDING LOGO
            with dpg.drawlist(width=500, height=100):
                    dpg.draw_image("image_id", (0, 0), (500, 200), uv_min=(0, 0), uv_max=(1, 1))
            
            # ADDING LANDING TEXT
            dpg.add_text('\t\t\t\tWelcome to Simple Addon Manager!')
            dpg.add_text('\t  Enable or Disable your Addons using the checkbox below :)')
            dpg.add_separator()

            default_pkg_list = Content_XML().get_custom_pkg_list_list(None, None)[4]
            ms_pkg_list_list = Content_XML().get_custom_pkg_list_list(None, None)[2]
            asobo_pkg_list = Content_XML().get_custom_pkg_list_list(None, None)[1]
            custom_pkg_list = Content_XML().get_custom_pkg_list_list(None, None)[0]
            
            total_pkg_status = dict()
            total_pkg_status['Total Packages']   = len(asobo_pkg_list) + len(custom_pkg_list) + len(ms_pkg_list_list)
            total_pkg_status['Enabled Packages'] = get_total_pkg_status()[0] - len(default_pkg_list) 
            total_pkg_status['Disabled Packages'] = get_total_pkg_status()[1]
            
            for key,values in total_pkg_status.items():
                print(key,values)

            with dpg.table(header_row=False, row_background=True,
                   borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True):

                # use add_table_column to add columns to the table,
                # table columns use child slot 0
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()

                # add_table_next_column will jump to the next row
                # once it reaches the end of the columns
                # table next column use slot 1
                with dpg.table_row():
                       for keys,values in total_pkg_status.items():
                            dpg.add_text(f"{keys} = {values} ")
                            
                            
                
                


            #Search_Bar.add_earch_bar()
            dpg.add_separator()
            
            # PRINTING CUSTOM PKG LIST
            dpg.add_text('Custom Scenery')
            dpg.add_separator()
            Content_XML().get_pkg_list(custom_pkg_list)
            dpg.add_separator()
            
            
            dpg.add_text('Asobo Scenery')
            dpg.add_separator()
            Content_XML().get_pkg_list(asobo_pkg_list)
            dpg.add_separator()

            # PRINTING MS PKG LIST
            dpg.add_text('Microsoft Scenery')
            dpg.add_separator()
            Content_XML().get_pkg_list(ms_pkg_list_list)
            dpg.add_separator()
          
            #dpg.show_item_registry()

            dpg.create_viewport(title=self.app_title, width=self.width, height=self.height)
            dpg.set_primary_window("Primary Window", True)
            dpg.set_viewport_small_icon("img\icon.ico")
            dpg.setup_dearpygui()
            dpg.show_viewport()
            dpg.start_dearpygui()

            # below replaces, start_dearpygui()
            while dpg.is_dearpygui_running():
                # insert here any code you would like to run in the render loop
                # you can manually stop by using stop_dearpygui()
                dpg.render_dearpygui_frame()

            dpg.destroy_context()
    

class Toolbar:
    def __init__(self):
        with dpg.viewport_menu_bar():
                with dpg.menu(label='File'):
                    dpg.add_menu_item(label='Save', callback=None)
                    dpg.add_menu_item(label='Exit', callback=lambda: dpg.destroy_context())
                
                with dpg.menu(label='Help'):
                    dpg.add_menu_item(label="About", callback=lambda : webbrowser.open('https://www.facebook.com/TailstrikeDesigns'))
                    dpg.add_menu_item(label="Github", callback=lambda : webbrowser.open('https://www.github.com'))


class Content_XML():               

    def get_custom_pkg_list_list(self, sender, data) -> list:
        custom_pkg_list = list()
        default_pkg = list()
        asobo_pkg = list()
        microsoft_pkg = list()
        for elem in CONTENT_XML_ROOT.iter():
            pkg_name = elem.get('name')

            if 'fs-base' in str(pkg_name):
                default_pkg.append(pkg_name)

            elif 'asobo' in str(pkg_name):
                asobo_pkg.append(pkg_name)

            elif 'microsoft' in str(pkg_name):
                microsoft_pkg.append(pkg_name)
            
            else:
                custom_pkg_list.append(pkg_name)  

        custom_pkg_list.remove(None)

        custom_pkg_list.sort()
        
        total_pkg_list = custom_pkg_list + asobo_pkg

        return ([custom_pkg_list, asobo_pkg, microsoft_pkg, total_pkg_list, default_pkg])
 
    def get_pkg_list(self, pkg):
        for pkg_idx in range(0,len(pkg)): 
            pkg_default_state = (Content_XML().get_pkg_status(pkg[pkg_idx]))
            dpg.add_checkbox(label=pkg[pkg_idx], callback=Content_XML().change_pkg_status, default_value= pkg_default_state)
        return ([pkg[pkg_idx]]) 
    

    def get_pkg_status(self, pkg_name:str) -> bool:
        for subelem in CONTENT_XML_ROOT.findall('Package'):
            if pkg_name == subelem.get('name'):
                if (subelem.get('active')) == 'true': return True 
                else: return False
                

    def change_pkg_status(sender, data):
        curr_pkg = str((dpg.get_item_label(data)))
        
        state =not(get_active_state(curr_pkg)) 
        
        #print(curr_pkg, data, state)
       
        for subelem in CONTENT_XML_ROOT.findall('Package'):
            if curr_pkg == subelem.get('name'):
                subelem.set('active', str(state).lower() )
                CONTENT_XML.write(WINDOWS_CONTENT_XML_PATH)
                #print(subelem.get('name'), subelem.get('active'))
                
    
class Search_Bar:
    def add_earch_bar():
        search_id = dpg.add_input_text(label='',  callback=get_search_input  , hint="Type to search...",  on_enter=False)


class Custom_Window:
        def add_window(self, search_bar_title, width, height):
                self.search_bar_title = search_bar_title
                self.width = width
                self.height = height
                with dpg.window(label=self.search_bar_title, width=self.width, height=self.height, tag="Secondary Window"):
                    pass


if __name__ == "__main__":
    App('Simple MFS Addon Manager', 540, 720).main_window()