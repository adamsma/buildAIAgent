from functions.get_files_info import get_files_info

print(get_files_info("calculator", "."), "\n\n")

print(get_files_info("calculator", "pkg"), "\n\n")

print(get_files_info("calculator", "/bin"), "\n\n")

print(get_files_info("calculator", "../"), "\n\n")