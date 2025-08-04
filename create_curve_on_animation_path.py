import maya.cmds as cmds

def create_curve_on_animation_path():
    """
    選択したトランスフォームノードのアニメーションパスに沿ってカーブを作成する。
    """
    # 選択したオブジェクトを取得
    selected_objects = cmds.ls(selection=True, type='transform')
    # 選択されているオブジェクトがない場合は警告を出して終了
    if not selected_objects:
        cmds.warning('トランスフォームノードを選択してください。')
        return
    # 複数のオブジェクトが選択されている場合は最初のオブジェクトを使用
    for target_object in selected_objects:
        # シーンのタイムレンジを取得
        start_time = int(cmds.playbackOptions(query=True, minTime=True))
        end_time = int(cmds.playbackOptions(query=True, maxTime=True))
        # カーブのポイントを格納するリスト
        curve_points = []
        # タイムラインをループして各フレームのオブジェクトの位置を取得
        for frame in range(start_time, end_time + 1):
		    # 現在のフレームに移動
            cmds.currentTime(frame, edit=True)
            # オブジェクトのワールドスペースでの位置を取得
            position = cmds.xform(target_object, query=True, translation=True, worldSpace=True)
            
            # リストに位置を追加
            curve_points.append(position)
        # 取得したポイントからカーブを作成
        if curve_points:
            cmds.curve(point=curve_points, degree=1, name=f"{target_object}_animation_path_curve")
            cmds.warning(f"アニメーションパスに沿ったカーブが作成されました: {target_object}_animation_path_curve")
        else:
            cmds.warning('位置データを取得できませんでした。オブジェクトにアニメーションキーがあるか確認してください。')
# スクリプトを実行
if __name__ == '__main__':
    create_curve_on_animation_path()
