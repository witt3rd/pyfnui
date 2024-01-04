"""
This file contains the implementation of a Streamlit application for managing Python functions.

The full function definition is:
{
  "name": "string",
  "description": "string",
  "code": "string",
  "pkg_dependencies": [
    "string"
  ],
  "fn_dependencies": [
    "string"
  ],
  "args": [
    {
      "name": "string",
      "type": "string",
      "description": "string"
    }
  ],
  "created_at": "2024-01-03T19:02:59.097Z",
  "updated_at": "2024-01-03T19:02:59.097Z"
}

"""

# System imports
import json
import os
import requests

# Third-party imports
from dotenv import load_dotenv
from icecream import ic
import pandas as pd
import streamlit as st

#

load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")

#

if "server_url" not in st.session_state:
    st.session_state.server_url = SERVER_URL

if "page" not in st.session_state:
    st.session_state.page = "home"

if "function_name" not in st.session_state:
    st.session_state["function_name"] = None

if "summaries" not in st.session_state:
    response = requests.get(SERVER_URL + "/functions/summaries")
    if response.status_code == 200:
        st.session_state.summaries = response.json()

if "summary_names" not in st.session_state:
    st.session_state.summary_names = sorted(
        [s["name"] for s in st.session_state.summaries]
    )

#

st.sidebar.text_input("Server URL", key="server_url")

st.title("Python Function Server")

# Helpers


def reset_summaries() -> None:
    del st.session_state.summaries
    del st.session_state.summary_names


def list_to_str(lst: list[str]) -> str:
    return ",".join(lst)


def str_to_list(string) -> list[str]:
    return string.split(",")


# Pages
ic(st.session_state.page)

if st.session_state.page == "home":
    st.subheader("Functions")

    def on_click_new() -> None:
        st.session_state.function_name = None
        st.session_state.update({"page": "create_or_edit"})

    st.button(
        label="New",
        type="secondary",
        use_container_width=True,
        on_click=on_click_new,
    )

    if (
        st.session_state.get("function_name") is None
        and len(st.session_state.summary_names) > 0
    ):
        st.session_state.function_name = (
            st.session_state.selectbox_function_name
        ) = st.session_state.summary_names[0]

    st.selectbox(
        label="Select a function",
        options=[fn_summary["name"] for fn_summary in st.session_state.summaries],
        key="selectbox_function_name",
    )
    for summary in st.session_state.summaries:
        st.session_state.function_name = st.session_state.selectbox_function_name
        if summary["name"] == st.session_state.selectbox_function_name:
            st.write("Description")
            st.write(summary["description"])

            col1, col2 = st.columns(2)
            with col1:
                st.button(
                    label="Edit or Delete",
                    use_container_width=True,
                    on_click=lambda: st.session_state.update(
                        {"page": "create_or_edit"}
                    ),
                )
            with col2:
                st.button(
                    label="Execute",
                    use_container_width=True,
                    on_click=lambda: st.session_state.update({"page": "execute"}),
                )


if st.session_state.page == "create_or_edit":
    st.button(
        label="🏠",
        type="secondary",
        on_click=lambda: st.session_state.update({"page": "home"}),
    )

    function_details = {
        "name": "",
        "description": "",
        "code": "",
        "pkg_dependencies": [],
        "fn_dependencies": [],
        "args": [],
    }

    function_name = st.session_state.function_name
    if function_name:
        st.subheader("Edit Function")
        response = requests.get(SERVER_URL + "/functions/" + function_name)
        if response.status_code == 200:
            function_details = response.json()
    else:
        st.subheader("Create Function")

    name = st.text_input("Name", function_details["name"])
    description = st.text_area("Description", function_details["description"])
    code = st.text_area("Code", function_details["code"])
    pkg_dependencies_str = st.text_input(
        label="Package Dependencies",
        value=list_to_str(function_details["pkg_dependencies"]),
        placeholder="comma separated list of Python packages",
    )
    fn_dependencies_str = st.text_input(
        label="Function Dependencies",
        value=list_to_str(function_details["fn_dependencies"]),
        placeholder="comma separated list of Python functions",
    )

    st.write("Arguments")
    args_df = pd.DataFrame(function_details["args"])
    args_df = args_df.reindex(columns=["name", "type", "description"])
    args_df = args_df.astype(str)
    args_edited_df = st.data_editor(
        data=args_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
    )
    if name and description and code:
        args_list = []
        for index, row in args_edited_df.iterrows():
            arg = {
                "name": row["name"],
                "type": row["type"],
                "description": row["description"],
            }
            args_list.append(arg)
        new_function = {
            "name": name,
            "description": description,
            "code": code,
            "pkg_dependencies": str_to_list(pkg_dependencies_str)
            if pkg_dependencies_str
            else [],
            "fn_dependencies": str_to_list(fn_dependencies_str)
            if fn_dependencies_str
            else [],
            "args": args_list,
        }
        if function_name:
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    label="Delete",
                    use_container_width=True,
                    type="primary",
                ):
                    response = requests.delete(
                        SERVER_URL + "/functions/" + function_name
                    )
                    if response.status_code == 200:
                        st.success("Function deleted successfully")
                        reset_summaries()
                    else:
                        st.error("Failed to delete function")
            with col2:
                if st.button(
                    label="Update",
                    use_container_width=True,
                ):
                    response = requests.post(
                        SERVER_URL + "/functions", json=new_function
                    )
                    if response.status_code == 200:
                        st.success("Function updated successfully")
                        reset_summaries()
                    else:
                        st.error("Failed to update function")
        else:
            if st.button(
                label="Add",
                use_container_width=True,
            ):
                response = requests.post(SERVER_URL + "/functions", json=new_function)
                if response.status_code == 201:
                    st.success("Function created successfully")
                    reset_summaries()
                else:
                    st.error("Failed to create function")


if st.session_state.page == "execute":
    st.button(
        label="🏠",
        type="secondary",
        on_click=lambda: st.session_state.update({"page": "home"}),
    )

    st.subheader("Execute Function")

    function_name = st.session_state.function_name

    response = requests.get(SERVER_URL + "/functions/" + function_name)
    if response.status_code == 200:
        function_details = response.json()

        st.write("`" + function_details["name"] + "`")
        st.write(function_details["description"])

        if len(function_details["args"]) == 0:
            st.write("No arguments")
        else:
            st.write("Arguments")
            for arg in function_details["args"]:
                st.text_input(
                    label=arg["name"],
                    placeholder=arg["type"],
                    help=arg["description"],
                    key="arg_" + arg["name"],
                )
        if st.button("Execute"):
            if len(function_details["args"]) == 0:
                args = None
            else:
                args = [
                    {
                        "name": arg["name"],
                        "value": st.session_state["arg_" + arg["name"]],
                    }
                    for arg in function_details["args"]
                ]
                # remove empty args (i.e., args with no value)
                args = [arg for arg in args if arg["value"]]
            ic(args)
            response = requests.post(
                SERVER_URL + "/functions/" + function_name + "/execute/",
                json=args,
            )
            if response.status_code == 200:
                try:
                    result = response.json()
                except ValueError:
                    result = response.text
                st.write("Result")
                st.write(result)
            else:
                st.error("Failed to execute function")
