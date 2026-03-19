

# def offline_data():
#     file_name = "Former Words of the day"
#     try:
#         if os.path.exists(file_name):
#             with open(file_name, "r") as f:
#                 new_data = json.loads(f.read())
#                 return new_data
#
#             # with open(file_name, "w") as f:
#             #     f.write(json.dumps(new_data))
#
#     except ValueError:
#         messagebox.showerror("Error", "Something went wrong.")
#
# def extract_line(data):
#     for entry in data:
#         if 'vis' in entry['def'][0][0][1]:
#             for vis in entry['def'][0][0][1]['vis']:
#                 if 't' in vis and 'paean' in vis['t']:
#                     return vis['t']
#     return None
#
# def grab_dt(data):
#     results = []
#     for entry in data:
#         for sense in entry['def']:
#             for sseq in sense['sseq']:
#                 for item in sseq:
#                     if 'dt' in item[0]:
#                         for dt in item[1]['dt']:
#                             results.append(dt[1][0]['vis'][0]['t'])
#     return results
#
#
# def pull_specific_video(folder_path, video_name):
#     # Default case (equivalent to else)
#     photo_path = os.path.join(folder_path, video_name)
#     if os.path.exists(photo_path):
#         return Image.open(photo_path)
#     else:
#         raise FileNotFoundError(f"The photo '{video_name}' does not exist in the specified folder.")
#
#
# today_video = play_video(r"Photos", f"{WORD}.mp4")
# st.video(today_video)