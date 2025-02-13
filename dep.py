from openai import OpenAI
import json
def get_completion(prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "developer", "content": "You are a assistant specializing in computer science, particularly evaluation of code. Whenever you are given a task you reason clearly and unambiguously to arrive at an answer. Instead of rushing to an answer you think the problem through even if it takes more time than usual. You are not too verbose. Your answers are short with all the necessary information included. If you do not know the answer of a particular question you simply reply with 'I do not know'"},
        {"role": "user", "content": prompt}
    ]
    )
    return (completion.choices[0].message.content)

def getDepth(code):
    # get the depth of the code
    # return the depth
    prompt=f"get the depth of the code delimited by triple backticks. Depth of the code is defined as nesting level of predefined constructs. The constructs that are considered as a new level are as follows:- a loop, assignment of a variable, defining a class, defining a function/method, a conditional using if-else or a switch call. Return a single number - the depth of the given code. Do not attach any pre or post text like depth is etc.  ```{code}```"
    ans = get_completion(prompt)
    return int(ans)

def codeDecomposition(code):
    # break code into subcodes using AST. ast in python can only be used for python files. 
    # suggested by chatGPT
    # return a list of the subcodes
    prompt=f""" You are given a code snippet. You need to break the code into subcodes. One subcode ends and another subcode starts when there is a loop, defining a class, defining a function/method, a conditional using if-else or a switch call. Only decompose codes on the initial level of the code's AST. Whatever is nested inside the first level is part of the subcode. The decomposition must be exhaustive, ensuring that every line, symbol, and punctuation mark in the original code is explicitly included in one of the defined subcodes, leaving no element unaccounted for. Return the subcodes in a JSON format with the key 'subcodes' and the corresonding value to be array of the subcodes. Do not attach any pre or post text like subcodes are etc. DO NOT alter the code in any way,shape or form. Just return the exact sub code snippet in the array.    ```{code}```
    """
    json_string = get_completion(prompt)
    data=json.loads(json_string)
    ans=data['subcodes']
    return ans

def getDependencies(code):
    # get the dependencies of the code
    # return a list of dependencies
    example = """class RunsComparator implements Comparator<Player> {
    @Override
    public int compare(Player p1, Player p2) {
        // Question 1: Write code for comparing/sorting runs in descending order [Total: 2 marks]
        // Return a negative value if the first player has more runs, 
        // a positive value if the second player has more runs, or zero if they have the same number of runs.
        return Integer.compare(p2.getRunsScored(), p1.getRunsScored());
    }
    }"""

    prompt = f"""
    The aim is to get the user defined dependencies of the code delimited by triple backticks. To achieve this follow the below steps:
    Step 1:look at the code and understand which programming language it is written in. 
    Step 2: Keep referring to that language's documentation when finding the dependencies
    Step 3: Analyse the code one line at a time like a human would do and keep a track of user defined variables and methods that you do not understand
    Step 4: The user defined variables and methods you do not understand are dependencies of a code as the code cannot be comprehended without them.
    
    For example if I have a java code as:
    {example}

    We do not know what Player is or any of its properties. We do not know what the getRunsScored method is either so these are considered
    as the dependencies of the above code.
    However inbulit functions of the language such as Integer.compare() are not dependencies as we know what it does 
    as it is included in the documentation.

    Similarly find out the dependencies for the code {code}

    Step 5: Return all the dependencies and the programming language in the form of a comma seperated list only. This list should strictly only contain the names of methods or 
    class of objects it does not understand.
    Do not return anything except for this list."""
    ans = get_completion(prompt)
    return ans 

def retrieveSemantics(dependencies):
    # get the semantics of the dependencies
    # return a dictionary of the dependencies and their semantics
    """If the code is semantically correct, each external
    dependency should have been previously analyzed and exist in
    the Semantic Dependency Decoupling Storage unit. We simply
    need to search and retrieve the semantics associated with
    each external dependency variable. The semantic descriptions
    (DPsemantics) of these external dependencies, retrieved from
    the Semantic Dependency Decoupling Storage unit, is then
    combined with the SC and inputted into the LLM for analysis."""
    dependencySemantics={}
    for DP in dependencies:
        if DP in storage:
            dependencySemantics[DP]=storage[DP]
        else :
            print(f"Dependency not found in storage for {DP}")            
    return dependencySemantics

def LLM(code,dependencySemantics,subCodesSemantics=None):    
    # use the LLM to get the semantics of the code
    # return the semantics of the code
    prompt = f""" The aim is to get the semantics of the code delimited by triple backticks
    given the semantics of user defined dependencies and the semantics of subcodes if there are any.
    You are required to refer to {dependencySemantics} for meaning of user defined dependencies in the code. It is a a dictionary of the dependencies and their semantics.
    You are required to refer t{subCodesSemantics}  for the meaning of subcodes present in the code. It is a list of the semantics of the subcodes of the given code.
    Keeping the above meanings in mind, find the semantics of {code}. 
    The output should strictly be in a string format that contains the meaning of the code. Do not make up any answers and if 
    you are confused just say you don't know. Do not return the semantics of user-defined dependencies and subCode smeantics.
    """
    ans = get_completion(prompt)
    return ans

def updateSemantic(dependency,subCodesSemantic):
    # update the semantic of the dependency using the semantic of the subcodes
    # return the updated semantic
    prompt=f"""You are given the semantic of a dependency and the semantic of the subcode. Using these semantics, update the semantic of the dependency. The semantic of the dependency is delimited by triple backticks. The semantic of the subcode is delimited by double backticks. Return the updated semantic of the dependency. Do not attach any pre or post text like semantics are etc. Semantics of the dependency: ```{dependency}``` Semantics of the subcode: ``{subCodesSemantic}``  """
    ans = get_completion(prompt)
    return ans


def summarizeSemantic(subCodesSemantics):
    # summarize the semantics of the subcodes
    # return the summarized semantic
    prompt=f"""You are given semantics of various subcodes. Using these semantics, summarize the semantics of the entire code. The semantics of the subcodes are delimited by triple backticks and are given as a list. Return the summarized semantics of the entire code. Do not attach any pre or post text like semantics are etc. ``````{subCodesSemantics}`````  """
    ans = get_completion(prompt)
    return ans

    
def getSemantic(code):
    storage={}
    subCodes=codeDecomposition(code)
    subCodesSemantics=[]
    for SC in subCodes:
        SCDepth=getDepth(SC)
        dependencies=getDependencies(SC)
        dependencySemantics=retrieveSemantics(dependencies)
        if SCDepth<3:
            subCodesSemantic=LLM(SC,dependencySemantics)
        else:
            SSCSemantics=getSemantic(SC)
            subCodesSemantic=LLM(SC,dependencySemantics,SSCSemantics)
        subCodesSemantics.append(subCodesSemantic)
        for DP in dependencySemantics:
            newDependency=updateSemantic(DP,subCodesSemantic)
            storage.update(newDependency)
    codeSemantic=summarizeSemantic(subCodesSemantics)
    return codeSemantic    



 

