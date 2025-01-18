def stitch_finder(text):
    """
    Detect substrings using a sliding window.

    :param text: The input string to search.
    :param targets: A list of target substrings to detect.
    :return: A list of lists, each containing detected substrings with their numbers for each line.
    """
    # Normalize the text and targets for case-insensitive search
    text = text.lower()
    text_result = ""
    targets = ["sc", "ch", "dc", "hdc", "tc", "mr", "inc", "dec", "blo", "flo", "slst", "x"]

    # Split the text into lines
    lines = text.splitlines()

    # Initialize results
    all_results = []

    # Sliding window approach
    window_size = max(len(target) for target in targets)  # Max length of target substrings

    repeat = False
    toadd = []

    for line in lines:
        wordcount = 0
        if line:
            line_results = []
            line += '   '
            line = line.replace('sl st', 'slst')
            
            i = -1
            while i < len(line) - window_size:
            #for i in range(len(line) - window_size + 1):
                i += 1
                #print(i, line[i], line_results)
                if line[i] == ' ' and i < len(line) -1 and line[i+1] != ' ':
                    wordcount += 1
                    #print('hello')
                    continue

                # Extract the current window
                window = line[i:i + window_size]
                if window.startswith('[') or window.startswith('('):
                    repeat = True
                    
                elif window.startswith(']') or window.startswith(')'):
                    if toadd:
                        line_results.append(toadd)
                    toadd = []
                    repeat = False
                #print(window)
                # Check for any target in the window
                for target in targets:

                    
                    if window.startswith(target):
                        # Ensure the characters before and after are not letters
                        before = line[i - 1] if i > 0 else " "
                        after = line[i + len(target)] if i + len(target) < len(line) else " "

                        if not before.isalpha() and not after.isalpha():
                        # Extract the number before the target
                            if target == "x":
                                num_start = i + 1
                                while num_start < len(line) and (line[num_start].isdigit() or line[num_start] == ' '):
                                    num_start += 1

                                number = int(line[i+1:num_start].strip())
                                #print(number)
                                torepeat = line_results[-1]
                                line_results.pop()
                                count = torepeat[0][1]
                                for j in range(number):
                                    
                                    for item, oldcount in torepeat:
                                        line_results.append((item, count))
                                        count += 1
                                        if j != number-1:
                                            line = line[:i] + item + ' ' + line[i:]
                                            print(i)
                                            i += len(item) + 1

                                #result = f"{target}{number}".strip()
                                #line_results.append(result)
                                num_start = i + 1
                                while num_start < len(line) and (line[num_start].isdigit() or line[num_start] == ' '):
                                    num_start += 1
                                
                                line = line[:i] + line[num_start:]
                                #print(torepeat, line_results)

                                break

                            else:
                                num_start = i - 1
                                while num_start >= 0 and (line[num_start].isdigit() or line[num_start] == ' '):
                                    #print('hi')
                                    num_start -= 1

                                
                                if num_start < i - 1:
                                    
                                    number = line[num_start + 1:i].strip() 
                                    if line[i-1] == ' ':
                                        line = line[:i-1] + line[i:]
                                        wordcount -= 1
                                else:
                                    number = ""

                                # Exclude matches where the characters before (excluding spaces) are "th", "nd", or "st"
                                context_start = max(0, num_start - 2)
                                context = line[context_start:num_start + 1].strip()

                                if context not in ["th", "nd", "st"]:
                                    
                                    result = f"{number}{target}".strip()
                                    if repeat:
                                        toadd.append((result, wordcount))
                                    else:
                                       
                                        line_results.append((result, wordcount))
                                        #print("window", window, line, line[i], i)
                                        #print(line_results)
                                break  # Move to the next window after finding a match
                
                
            if line_results:
                all_results.append(line_results)
            
            line = line.replace('\t', ' ')[:-3]
            
            text_result += line + '\n'

        
    return (text_result[:-1], all_results)