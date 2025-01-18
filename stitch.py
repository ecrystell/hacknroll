def stitch_finder(text):
    """
    Detect substrings using a sliding window.

    :param text: The input string to search.
    :return: A list of lists, each containing detected substrings with their numbers for each line.
    """

    targets = ["sc", "ch", "dc", "hdc", "tc", "mr", "inc", "dec", "blo", "flo", "slst", "sl st", "x"]

    # Normalize the text and targets for case-insensitive search
    text = text.lower()
    text_result = ""
    targets = [target.lower() for target in targets]

    # Split the text into lines
    lines = text.splitlines()

    # Initialize results
    all_results = []

    # Sliding window approach
    window_size = max(len(target) for target in targets)  # Max length of target substrings

    smaller = False
    for line in lines:
        if line:
            line_results = []
            line += '   '
            for i in range(len(line) - window_size + 1):
                # Extract the current window
                window = line[i:i + window_size]
                #print(window)
                # Check for any target in the window
                for target in targets:
                    if window.startswith('[') or window.startswith('('):
                        toadd = []
                        smaller = True
                    elif window.startswith(']') or window.startswith(')'):
                        if toadd:
                            line_results.append(toadd)
                        toadd = []
                        smaller = False


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

                                number = line[i+1:num_start].strip()
                                result = f"{target}{number}".strip()
                                line_results.append(result)
                                break

                            else:
                                num_start = i - 1
                                while num_start >= 0 and (line[num_start].isdigit() or line[num_start] == ' '):
                                    num_start -= 1

                                
                                if num_start < i - 1:
                                    number = line[num_start + 1:i].strip() 
                                    line = line[:i-1] + line[i:]
                                else:
                                    number = ""

                                # Exclude matches where the characters before (excluding spaces) are "th", "nd", or "st"
                                context_start = max(0, num_start - 2)
                                context = line[context_start:num_start + 1].strip()

                                if context not in ["th", "nd", "st"]:
                                    if not number and target not in ["flo", "blo", "mr"]:
                                        number = "1"
                                    result = f"{number}{target}".strip()
                                    if smaller:
                                        toadd.append(result)
                                    else:
                                        line_results.append(result)
                                break  # Move to the next window after finding a match
            if line_results:
                all_results.append(line_results)

            line = line.replace('\t', ' ')[:-3]
            
            text_result += line + "\n"
        
    return (text_result[:-1], all_results)


