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

def LLM(code,dependencies,subCodesSemantics=None):
    # use the LLM to get the semantics of the code
    # return the semantics of the code

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



 

