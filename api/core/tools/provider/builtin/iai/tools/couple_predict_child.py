from typing import Any, Union

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.provider.builtin.iai.tools.common import base64_to_binary, file_to_base64, run
from core.tools.tool.builtin_tool import BuiltinTool


class CouplePredictChildTool(BuiltinTool):
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any]
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        base_url = self.runtime.credentials.get("base_url", "")
        if not base_url:
            return self.create_text_message("Please input base_url")
        
        api_key = self.runtime.credentials.get("api_key", "")
        if not api_key:
            return self.create_text_message("Please input api_key")
        
        images = tool_parameters.get("images", []) 
        if not images or len(images) != 2:
            return [
                self.create_text_message(f"Please input father_image and mother_image, got {len(images)} images")
            ]
        image1 = file_to_base64(images[0])
        image2 = file_to_base64(images[1])
        payload = {
            "flow": 'couple_predict_child',
            "params": {
                "image1": image1,
                "image2": image2,
            }
        }
        try: 
            response = run(base_url, api_key, payload)
            images = response.get("images", [])
            ret = []
            for image in images:
                ret.append(self.create_blob_message(
                    blob=base64_to_binary(image['data']),
                    meta={"mime_type": "image/png"},
                    save_as=self.VariableKey.IMAGE.value,
                ))
            return ret
        except Exception as e:
            print(e)
            return [self.create_text_message("something went wrong")]
