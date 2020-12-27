import math

class Directory_Manager:
  def __init__(self, root_path, row_per_page):
    self.ROOT_PATH = root_path
    self.ROW_PER_PAGE = row_per_page
    self.path_stack = [self.ROOT_PATH]
    self.highlighted_file_stack = []

    # setup initial value
    dir_list = self.get_full_dir_list()
    if len(dir_list) == 0:
      self.highlighted_file_stack.append("empty")
    else:
      self.highlighted_file_stack.append(dir_list[0])

  # get all folders and files in current path
  def get_full_dir_list(self):
    folder_list = []
    file_list = []
    directory_list = []
    current_path = self.path_stack[len(self.path_stack) - 1]

    for file in current_path.iterdir():
      if file.is_dir():
        folder_list.append(file)
      elif file.suffix == ".py" or file.suffix == ".sh": # filter only '.py' & '.sh' scripts
        file_list.append(file)
        
    # folder_list.sort(key=sort_by_name)
    folder_list_sorted = sorted(folder_list)
    file_list_sorted = sorted(file_list)

    directory_list.extend(folder_list_sorted)
    directory_list.extend(file_list_sorted)

    return directory_list

  # get the scoped menu based on currently highlighted file
  def get_menus(self):
    dir_list = self.get_full_dir_list()
    highlighted_file = self.get_highlighted_path()

    if highlighted_file == "empty":
      return []

    if self.is_highlighted_path_exist():
      highlighted_file_idx = dir_list.index(highlighted_file)
      page_idx = (highlighted_file_idx + 1) / self.ROW_PER_PAGE
      if math.floor(page_idx) == page_idx:
        return self.get_paginated_dir_list(dir_list, math.floor(page_idx) - 1)
      else:
        return self.get_paginated_dir_list(dir_list, math.floor(page_idx))
    else:
      # TODO - handle this
      print("highlighted file not exist!")
  
  def highlight_previous_file(self):
    dir_list = self.get_full_dir_list()
    highlighted_file = self.get_highlighted_path()

    # TODO - check if `dir_list` is empty 

    if self.is_highlighted_path_exist():
      highlighted_file_idx = dir_list.index(highlighted_file)
      if highlighted_file_idx == 0:
        highlighted_file_idx = len(dir_list) - 1
      else:
        highlighted_file_idx = highlighted_file_idx - 1
      self.highlighted_file_stack.pop()
      self.highlighted_file_stack.append(dir_list[highlighted_file_idx])
    else:
      self.highlighted_file_stack.pop()
      self.highlighted_file_stack.append(dir_list[0])

  def highlight_next_file(self):
    dir_list = self.get_full_dir_list()
    highlighted_file = self.get_highlighted_path()

    # TODO - check if `dir_list` is empty 

    if self.is_highlighted_path_exist():
      highlighted_file_idx = dir_list.index(highlighted_file)
      if highlighted_file_idx == len(dir_list) - 1:
        highlighted_file_idx = 0
      else:
        highlighted_file_idx = highlighted_file_idx + 1
      self.highlighted_file_stack.pop()
      self.highlighted_file_stack.append(dir_list[highlighted_file_idx])
    else:
      self.highlighted_file_stack.pop()
      self.highlighted_file_stack.append(dir_list[0])
  
  def go_into_folder(self):
    if self.is_highlighted_path_directory():
      self.path_stack.append(self.get_highlighted_path())
      dir_list = self.get_full_dir_list()
      if (len(dir_list) > 0):
        self.highlighted_file_stack.append(dir_list[0])
      else:
        self.highlighted_file_stack.append("empty")
  
  def go_out_from_folder(self):
    if len(self.highlighted_file_stack) > 1:
      self.highlighted_file_stack.pop()
      self.path_stack.pop()

  def is_highlighted_path_directory(self):
    highlighted_file = self.get_highlighted_path()
    return highlighted_file.is_dir()

  def is_highlighted_path_file(self):
    highlighted_file = self.get_highlighted_path()
    return highlighted_file.is_file()

  def is_highlighted_path_exist(self):
    highlighted_file = self.get_highlighted_path()
    return highlighted_file.exists()
  
  def get_highlighted_path(self):
    return self.highlighted_file_stack[len(self.highlighted_file_stack) - 1]

  def get_current_dir_path(self):
    return self.path_stack[len(self.path_stack) - 1]

  def get_paginated_dir_list(self, dir_list, page_idx):
    start_idx = page_idx * self.ROW_PER_PAGE
    end_idx = start_idx + self.ROW_PER_PAGE
    return dir_list[start_idx : end_idx]
